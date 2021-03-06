import json
import random

class PageEncoder (json.JSONEncoder):
    def default (self, o):
        return {type (o).__name__ : o.__dict__}

# Used to hold the content for and indicate a text only window
class Intro:
    def __init__(self):
        self.ptype = "Intro"

class TextWindow:
    def __init__(self, header, text, footer):
        self.header = header
        self.text = text
        self.footer = footer
        self.ptype = "TextWindow"
        
# Used to hold the data for and indicate a base recording window
class BaseRecording:
    def __init__(self, passage, output_file, text):
        self.passage = passage
        self.text = text
        self.output_file = output_file + '.wav'
        self.ptype = "BaseRecording"

class TrimAudio:
    def __init__(self, passage, wav_file):
        self.passage = passage
        self.wav_file = wav_file
        self.ptype = "TrimAudio"
        
# Used to hold the data for and indicate a timed recording window
class TimedRecording:
    def __init__(self, passage, subject, percentage, text):
        self.text = text
        self.odd = False
        self.passage = passage
        self.output_file = subject + '/' + subject + '-' + passage + "-" + str(percentage) + ".wav"
        self.percentage = percentage
        self.ptype = "TimedRecording"

# Used to indicate a questionaire page
class Survey:
    def __init__(self, output):
        self.output_file = output + '.csv'
        self.ptype = "Survey"
        self.count = 0

def add_passages(subject, content, text):
    for passage in text:
        for (name, twister) in passage.items():
            file_name = subject + '/' + subject + '-' + name
            content.append(BaseRecording(name, file_name, twister))
            content.append(Survey(file_name))
            content.append(TrimAudio(name, file_name))

def timed_passages(subject, text):
    sessions = []
    for passage in text:
        for (name, twister) in passage.items():
            for pcent in [0.95, 0.90, 0.85]:
                file_name = subject + '/' + subject + '-timed'
                sessions.append([TimedRecording(name, subject, pcent, twister),
                                Survey(file_name)])
    return sessions

def setup_study(subject):

    with open('passages.json') as data_file:
        text = json.load(data_file)

        content = []
        
        content.append(TextWindow("Welcome and thank you for participating in our experiment!", "First, we need a sample of your reading! The passage you will read is called \"The Rainbow Passage.\" When the passage is presented, press the spacebar when you start reading and press the spacebar again when you are finished reading.", "Are you ready? Press the RETURN for the passage to appear."))
    
        content.append(BaseRecording('rainbow',subject + '/' + subject + "-rainbow-text", text['rainbow'][0]['rainbow']))
    
        content.append(TextWindow("The First Phase",
                                 "Nice reading! Now, it's time for the first phase of our experiment. You will be presented with multiple reading tasks. Please read them out loud at your own natural pace. Before you start reading, press the spacebar. When you finish reading, press the spacebar.\n\nAfter each reading task, a series of statements will be presented, asking you to rate your experience. Please respond to each statement on a scale of 1 to 5 (1=low, 5=high). Once you have finished responding to the statements, please press the spacebar to start the next reading. Again, before you start reading, press the spacebar and when you finish reading, press the spacebar. If you have any questions about the task, please ask the examiner at this time.", "When you are ready to begin, press RETURN to start."))

        add_passages(subject, content, text['twisters'])
        add_passages(subject, content, text['anomalous'])

        content.append(TextWindow("The Second Phase", "Thank you for your cooperation so far! In this last part, a passage will be presented and your recording time will begin immediately. Please read as much as you can until the timer by the sentence disappears. Sometimes the timer unravels slowly, other times it may unravel quickly. Just read whatever you can before the timer and reading disappears.\n\nPlease press the spacebar if you finish reading the passage before the timer fully unravels. You will read sentences that you have previously read before.\n\nAfter each sentence, you will be asked to respond to similar statements about your experience on a scale of 1 to 5 (similar to the first part of this experiement). Upon completion of the last rating, a new reading task will be offered.", "Ready to begin? Press RETURN to start your first reading."))
        
        timed = []
        timed.extend(timed_passages(subject, text['anomalous']))

        for group in timed:
            for p in group:
                p.odd = True
            
        timed.extend(timed_passages(subject, text['twisters']))

        random.shuffle(timed)
        timed = [page for section in timed for page in section]

        content.extend(timed)

        content.append(TextWindow("", "Wow! You've made it through our entire experiment! Thank you so much for participating! If you have any questions, please ask the experimenter at this time.", ""))
        return content
