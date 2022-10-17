import mediapipe as mp


mp_hands = mp.solutions.hands

# Check if hand is pointing
def is_pointing_gesture(hand_landmarks):
    if hand_landmarks is None:
        return False

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

    middle_finger_tip = None
    middle_finger_mcp = None

    ring_finger_tip = None
    ring_finger_mcp = None

    pinky_finger_tip = None
    pinky_finger_mcp = None

    return False
