import cv2
import time
import pyttsx3
import threading
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.75)
    classifier = GestureClassifier()
    
    transcript = []
    last_gesture = None
    gesture_frames = 0
    STABILITY_FRAMES = 10  # Number of frames a gesture must be held
    
    print("Starting Sign Language Detector...")
    print("Press 'q' to quit and hear the transcript.")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from webcam.")
            break

        img = cv2.flip(img, 1) # Mirror image
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        current_gesture = None
        if len(lmList) != 0:
            current_gesture = classifier.classify(lmList)

        # Stability Check
        if current_gesture:
            if current_gesture == last_gesture:
                gesture_frames += 1
            else:
                last_gesture = current_gesture
                gesture_frames = 0
            
            if gesture_frames == STABILITY_FRAMES:
                # Add to transcript if it's different from the last added word
                if not transcript or transcript[-1] != current_gesture:
                    transcript.append(current_gesture)
                    print(f"Detected: {current_gesture}")
        else:
            gesture_frames = 0
            last_gesture = None

        # UI
        cv2.putText(img, f"Gesture: {current_gesture if current_gesture else 'None'}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        
        transcript_str = " ".join(transcript[-5:]) # Show last 5 words
        cv2.putText(img, f"Transcript: {transcript_str}", (10, 450), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

        cv2.imshow("Sign Language Detector", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    full_transcript = " ".join(transcript)
    print(f"Final Transcript: {full_transcript}")
    
    # Save to file
    with open("transcript.txt", "w") as f:
        f.write(full_transcript)
    
    # Speak aloud
    if full_transcript:
        print("Reading aloud...")
        speak_text(full_transcript)

if __name__ == "__main__":
    main()
