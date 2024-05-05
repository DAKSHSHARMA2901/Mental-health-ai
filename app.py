import random
from nltk.chat.util import Chat, reflections

patterns = [
    # Greetings
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I am doing well, thank you!', 'I am good, thanks for asking.']),
    (r'what\'s up|sup|what\'s new|how\'s it going', ['Not much, how about you?', 'Just taking it easy. You?']),

    # Farewells
    (r'quit|bye|exit', ['Goodbye!', 'Take care!', 'See you later!']),

    # Emotional expressions
    (r'i\'m (.*)', ["Tell me more about why you're {0}.", "It\'s okay to feel {0}."]),
    (r'(.*) (depressed|sad|anxious|lonely|stressed)', ['I\'m sorry to hear that. How can I help?',
                                                      'You are not alone. I\'m here to listen.']),
    (r'(.*) (happy|joyful|excited)', ['That\'s wonderful to hear! What brought you joy?',
                                      'It\'s great to see you happy! What made you feel this way?']),
    (r'(.*) (angry|frustrated|upset)', ['I\'m here for you. What\'s causing you to feel {1}?',
                                        'It\'s okay to feel {1}. Let\'s talk about what happened.']),

    # Needs and wants
    (r'i need (.*)', ['What do you need help with?', 'I\'m here to support you with this.']),
    (r'i want (.*)', ['Why do you want {0}?', 'What do you think it will do for you?']),
    (r'can you (.*)', ['I\'ll do my best. What specifically do you need help with?',
                      'What outcome are you hoping for by {0}?']),

    # Apologies
    (r'(.*) (sorry|apologize)', ['It\'s okay. What made you feel the need to apologize?',
                                 'Don\'t worry about it. What\'s on your mind?']),

    # Love and relationships
    (r'(.*) (love|loved|loving)', ['Love is a beautiful thing. What aspect of love are you thinking about?',
                                   'Love is important. Who or what are you feeling love towards?']),
    (r'(.*) (relationship)', ['Tell me more about your relationship.',
                                                          'How are things with your partner?']),

    # Requests for assistance or support
    (r'(.*) (help|support|talk to) me', ['Of course, I\'m here to help. What do you need?',
                                         'I\'m listening. What kind of support are you looking for?']),

    # Specific emotional expressions and needs
    (r'(.*) (feeling of sadness|feels so heavy|everything is going wrong in my life|feel low|feel like myself)',
     ['I\'m sorry to hear that you\'re feeling this way. Wanna talk about it?',
      'It\'s okay to feel sad sometimes. Wanna talk about it?',
      'Would you like to talk about what\'s been bothering you?',
      'I know it may not seem like it right now, but things can improve. It\'s important to take things one step at a time and focus on small victories.',
      'You\'re stronger than you think, and I believe in you.']),

    # Expressions related to feeling hopeless
    (r'(.*) (I just feel so hopeless|like nothing will ever get better|talk to)',
     ['I know it may not seem like it right now, but things can improve. It\'s important to take things one step at a time and focus on small victories.',
      'You\'re stronger than you think, and I believe in you.']),

    # Expression related to loss
    (r'(.*) (lost|died|expired|no more|dead)',
     ['Losing someone or something you care about is incredibly difficult.',
      'It\'s okay to feel the way you do. Grieving is a natural process, and everyone experiences it differently.']),

    # Expression related to relationship issues
    (r'(.*) (girlfriend|falling apart|lost)',
     ['I\'m so sorry to hear that you\'re going through this. It must be incredibly difficult. Do you want to talk about what\'s been happening?',
      'That sounds really tough. It\'s normal for relationships to have ups and downs, but it\'s important to communicate openly and honestly with each other. Have you tried talking to your partner about how you\'re feeling?',
      'That must be really frustrating. It\'s important to feel heard and supported in a relationship. Maybe it could help to try talking to them again, but']),

    # Patterns of questions and supportive responses
    (r'(.*) (confused|lost|uncertain)',
     ['It\'s okay to feel confused or lost sometimes. What specifically are you unsure about?',
      'Feeling uncertain is natural. Let\'s work through it together.']),
    (r'(.*) (overwhelmed|burdened|swamped)',
     ['Feeling overwhelmed can be tough. Let\'s break things down and tackle them one step at a time.',
      'I understand feeling overwhelmed. What tasks or responsibilities are weighing on you the most?']),
    (r'(.*) (scared|afraid|anxious|nervous)',
     ['It\'s normal to feel scared or anxious. What\'s causing you to feel this way?',
      'I\'m here to support you through your fears. Let\'s talk about what\'s making you anxious.']),
    (r'(.*) (unworthy|inadequate|not good enough)',
     ['You are worthy and deserving of love and respect. What makes you feel this way?',
      'Feeling inadequate is tough, but you are enough just as you are. Let\'s explore why you feel this way.']),
    (r'(.*) (rejected|neglected|alone)',
     ['Feeling rejected or alone is hard. You are not alone, and I\'m here to listen and support you.',
      'It\'s okay to feel this way. Let\'s talk about what triggered these feelings of rejection or loneliness.']),
    (r'(.*) (stuck|trapped)',
     ['Feeling stuck can be frustrating. Let\'s brainstorm together and find ways to move forward.',
      'We\'ll work together to find a way out of this feeling of being trapped. You\'re not alone in this.']),
    (r'(.*) (forgotten|ignored)',
     ['Feeling forgotten or ignored is difficult. Your feelings are valid, and I\'m here to listen and validate them.',
      'You\'re not forgotten, and your voice matters. Let\'s talk about how you\'re feeling and how we can address it.']),
    (r'(.*) (discouraged|disheartened|disappointed)',
     ['It\'s normal to feel discouraged sometimes. Let\'s focus on what you can control and find a way forward.',
      'I understand feeling disappointed. Let\'s talk about how we can turn things around and find hope together.']),
    (r'(.*) (hope|hopeless|desperate)',
     ['Feeling hopeless can be overwhelming, but there is always hope. I\'m here to remind you of your strength and resilience.',
      'You\'re not alone in feeling this way. Let\'s work together to find a glimmer of hope and a path forward.']),
       # Expressions related to failure
    (r'(.*) (failed|failure|unsuccessful)',
     ['Experiencing failure can be disheartening, but it doesn\'t define your worth. What happened?',
      'Failure is a part of life\'s journey. Let\'s explore what we can learn from this experience.']),
    (r'(.*) (disappointed|let down|didn\'t work)',
     ['I understand feeling disappointed. It\'s okay to feel this way. What were you hoping would happen?',
      'Feeling let down can be tough. Let\'s talk about what you were expecting and how we can move forward.']),
    (r'(.*) (mistake|wrong)',
     ['Making mistakes is human. What can you learn from this experience?',
      'We all make mistakes from time to time. Let\'s focus on how we can grow from this.']),
    (r'(.*) (regret|regretted)',
     ['Regret is a natural emotion. What decision do you wish you could change?',
      'It\'s normal to have regrets, but dwelling on them won\'t change the past. Let\'s focus on moving forward.']),
     (r'(.*) (give up|giving up|faith|faithless)',
     [' It sounds like you\'re feeling really discouraged right now. Can you tell me more about what\'s been going on?',
      'It\'s normal to have regrets, but dwelling on them won\'t change the past. Let\'s focus on moving forward.']),
   (r'how (.*)', ['What do you need help with?', 'I\'m here to support you with this.']),
    




      (r'(.*) (suicide|suicidal|dying|die)',
     [' You\'re not alone. I\'m here for you, and I\'m not going anywhere. We can get through this together. And if you\'re ever in immediate danger or need someone to talk to right away, there are hotlines and crisis services available 24/7.']),
     (r'(.*) (pain)',
     [' Have you considered seeing a healthcare professional? They might be able to provide some insight into the cause of your pain and offer treatment options,getting a proper diagnosis is important for finding the right treatment. It\'s better to address the issue early on rather than letting it worsen over time.']),
     
     (r'(.*) (headache)', ['I\'m sorry to hear you\'re experiencing a headache. Have you tried any remedies for it?', 
                      'Headaches can be tough. It might help to rest in a quiet, dark room and drink plenty of water.', 
                      'Sometimes a gentle massage or applying a cold compress to your forehead can help ease a headache. Would you like to try that?']),



]

chatbot = Chat(patterns, reflections)

def mental_health_companion():
    print("Welcome to the Mental Health Companion. How can I help you today?")
    while True:
        user_input = input("You: ")
        response = chatbot.respond(user_input)
        print("Companion:", response)
        if user_input.lower() in ['quit', 'bye', 'exit']:
            break

if __name__ == "__main__":
    mental_health_companion()