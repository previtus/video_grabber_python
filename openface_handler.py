import os
import cv2
import openface
import urllib
import numpy as np

class openface_handler(object):
    """
    Handles OpenFace

    some code from: https://github.com/platanus/openface-api/
    original openface: https://github.com/cmusatyalab/openface

    Download:
    - http://openface-models.storage.cmusatyalab.org/nn4.small2.v1.t7
    - http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

    """

    def __init__(self):
        dlibFacePredictor = "shape_predictor_68_face_landmarks.dat"
        self.align = openface.AlignDlib(dlibFacePredictor)
        networkModel = "nn4.small2.v1.t7"

        self.imgDim = 96
        self.coefs = [0.000, 0.000, 0.000, 0.000, 0.000, 0.027, 0.000, 0.000, 0.029, 0.000, 0.000, 0.054, 0.000, 0.004, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.038, 0.000, 0.020, 0.040, 0.000, 0.007, 0.000, 0.000, 0.047, 0.000, 0.031, 0.000, 0.015, 0.033, 0.000, 0.059, 0.000, 0.013, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.062, 0.000, 0.000, 0.000, 0.009, 0.066, 0.000, 0.002, 0.000, 0.025, 0.000, 0.000, 0.000, 0.000, 0.000, 0.001, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.057, 0.005, 0.000, 0.052, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.036, 0.000, 0.000, 0.011, 0.000, 0.000, 0.016, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.018, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.045, 0.000, 0.064, 0.042, 0.023, 0.000, 0.000, 0.000, 0.049, 0.000, 0.000, 0.000, 0.000]
        self.tholds = [0.05835, 0.04876, 0.02534, 0.03404, 0.05513, 0.06438, 0.04488, 0.02019, 0.06817, 0.06108, 0.00252, 0.04505, 0.03138, 0.09664, 0.03902, 0.04445, 0.03416, 0.02632, 0.05421, 0.03862, 0.06395, 0.00942, 0.04479, 0.07646, 0.06821, 0.07994, 0.00389, 0.04437, 0.06808, 0.05362, 0.06270, 0.00840, 0.05956, 0.05400, 0.00035, 0.04018, 0.00617, 0.08768, 0.03118, 0.03786, 0.05104, 0.03998, 0.05821, 0.03246, 0.05706, 0.08194, 0.04058, 0.03016, 0.05856, 0.09357, 0.08904, 0.06473, 0.05241, 0.04693, 0.06441, 0.01151, 0.05479, 0.01308, 0.00672, 0.05672, 0.04532, 0.01939, 0.04546, 0.05301, 0.05116, 0.08834, 0.07105, 0.05658, 0.06158, 0.03291, 0.02861, 0.07265, 0.01351, 0.05352, 0.00257, 0.04879, 0.05306, 0.04691, 0.02508, 0.07861, 0.05623, 0.05762, 0.06630, 0.05738, 0.03904, 0.03036, 0.00746, 0.01904, 0.02698, 0.04126, 0.04459, 0.03818, 0.04714, 0.02897, 0.08551, 0.01210, 0.04573, 0.07470, 0.00947, 0.03867, 0.04082, 0.03250, 0.03589, 0.08169, 0.01308, 0.01136, 0.03826, 0.02671, 0.02308, 0.01615, 0.05878, 0.02459, 0.04618, 0.03542, 0.04264, 0.06028, 0.04268, 0.07431, 0.06724, 0.05967, 0.00678, 0.03587, 0.01648, 0.03765, 0.06293, 0.03246, 0.05516, 0.06035]
        self.net = openface.TorchNeuralNet(networkModel, self.imgDim)
        np.set_printoptions(precision=2)

    def perform(self, img1, img2):
        dist = np.absolute(self.getRep(img1) - self.getRep(img2)) - self.tholds
        return np.dot(dist, self.coefs)

    def getRep(self, rgbImg):
        bb = self.align.getLargestFaceBoundingBox(rgbImg)

        if bb is None:
            print("Unable to find a face.")
            return False, None, None

        # aligned crop of image with the size of self.imgDim
        alignedFace = self.align.align(self.imgDim, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        if alignedFace is None:
            print("Unable to align image.")
            return False, None, None
        rep = self.net.forward(alignedFace)
        return True, rep, bb

    def getRepMulti(self, rgbImg):
        bbs = self.align.getAllFaceBoundingBoxes(rgbImg)

        if len(bbs) is 0:
            print("Unable to find a face.")
            return [False], [None], [None]

        successes = []
        reps = []
        for bb in bbs:
            # aligned crop of image with the size of self.imgDim
            alignedFace = self.align.align(self.imgDim, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

            if alignedFace is None:
                print("Unable to align image.")

                successes.append(False)
            else:
                successes.append(True)

            rep = self.net.forward(alignedFace)
            reps.append(rep)

        return successes, reps, bbs
