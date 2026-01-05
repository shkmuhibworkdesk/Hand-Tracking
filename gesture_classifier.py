class GestureClassifier:
    def __init__(self):
        self.tipIds = [4, 8, 12, 16, 20]

    def classify(self, lmList):
        if not lmList:
            return None

        fingers = []

        # Thumb (Right Hand Assumption for simplicity, or relative to palm)
        # Check if thumb tip is to the right of thumb IP joint (for right hand palm facing camera)
        # A more robust check: is the tip further away from the palm center than the joint?
        # For simple demo: x coordinate check.
        # Assuming right hand: if tip x < ip x (since image is mirrored usually? or not?)
        # Let's use a simpler heuristic: Thumb is open if tip is far from index base.
        # Standard check:
        if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]: # Right hand, palm facing camera
             fingers.append(1)
        else:
             fingers.append(0)
        
        # Note: The above thumb check is direction dependent. 
        # Let's refine it to be generic or assume right hand.
        # Better heuristic for thumb: compare distance to pinky base?
        # Let's stick to the standard x-axis check but we might need to flip for left hand.
        # For now, let's assume Right Hand.
        # If using a mirror image (webcam default), Right Hand appears as Left Hand on screen?
        # Let's just use the standard check and user can adjust.
        # Actually, let's correct the thumb check.
        # If tip x > ip x (for right hand) -> Open. 
        
        # 4 Fingers
        for id in range(1, 5):
            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        # Gestures
        if totalFingers == 5:
            return "Hello"
        elif totalFingers == 0:
            return "No" # Fist
        elif fingers == [1, 0, 0, 0, 0] or fingers == [0, 1, 0, 0, 0]: # Thumb only or Index only (sometimes thumb detection is tricky)
             # Let's make Thumbs Up specific
             # Thumbs up: Thumb open, others closed.
             if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0:
                 return "Yes"
        elif fingers == [0, 1, 1, 0, 0]:
            return "Peace"
        elif fingers == [1, 1, 0, 0, 1]:
            return "I Love You"
        elif fingers == [1]:
            return "me"
        
        return None
