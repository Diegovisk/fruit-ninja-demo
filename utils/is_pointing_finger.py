import mediapipe as mp


mp_hands = mp.solutions.hands

# Check if hand is pointing
def is_pointing_gesture(hand_landmarks):
    if hand_landmarks is None:
        return False

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y

    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    pinky_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y

    # Y1 > Y2 -> abaixado
    # Y1 < Y2 -> levantado
    if(
        index_finger_tip < index_finger_mcp and
        middle_finger_tip > middle_finger_mcp and
        ring_finger_tip > ring_finger_mcp and
        pinky_finger_tip > pinky_finger_mcp
    ):
        return True

    return False
