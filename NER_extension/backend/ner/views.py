from django.shortcuts import render

# Create your views here.



from django.http import JsonResponse
from .models import Paragraph

from django.views.decorators.csrf import csrf_exempt
import nltk
from .custom_crf import CustomCRF
import pickle


def word2features(sent, i,pos_tags_,entity_patterns,token_list,chunks):
    word = sent[i]
    
    if pos_tags_ != None:
        postag = pos_tags_[i]
    if pos_tags_ != None:
        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'postag': postag,
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
            'word.first_letter': word[0],
            'word.last_letter': word[-1],
            'has_ingsuffix': word.endswith('ing'),
            'prev_word': sent[i-1] if i > 0 else '<START>',
            'next_word': sent[i+1] if i < len(sent)-1 else '<END>',
            'prev_word_is_upper': sent[i-1].isupper() if i > 0 else False,
            'next_word_is_upper': sent[i+1].isupper() if i < len(sent)-1 else False,
            'pos_prefix': postag[:2],
            'pos_suffix': postag[-2:],
            'pos_category': postag[0],
            'word.is_all_uppercase': word.isupper(),
            'word.is_all_lowercase': word.islower(),
            'word.is_mixed_case': not word.isupper() and not word.islower(),
            'chunk':chunks[i],
            'prev_chunk': chunks[i-1] if i > 0 else '<START>',
            'next_chunk': chunks[i+1] if i < len(sent)-1 else '<END>',
            # 'induced_pattern_1': check_for_induced_pattern_1(word, sent),
            # 'induced_pattern_2': check_fors_induced_pattern_2(word, sent),
            # add additional induced patterns as necessary
        }
    else:
        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
            'word.first_letter': word[0],
            'word.last_letter': word[-1],
            'has_ingsuffix': word.endswith('ing'),
            'prev_word': sent[i-1] if i > 0 else '<START>',
            'next_word': sent[i+1] if i < len(sent)-1 else '<END>',
            'prev_word_is_upper': sent[i-1].isupper() if i > 0 else False,
            'next_word_is_upper': sent[i+1].isupper() if i < len(sent)-1 else False,
            'word.is_all_uppercase': word.isupper(),
            'word.is_all_lowercase': word.islower(),
            'word.is_mixed_case': not word.isupper() and not word.islower(),
            # 'induced_pattern_1': check_for_induced_pattern_1(word, sent),
            # 'induced_pattern_2': check_fors_induced_pattern_2(word, sent),
            # add additional induced patterns as necessary
        }
    if entity_patterns != None:
        token = token_list[i]
        passed_patterns = []
        for entity_in,patterns in entity_patterns.items():
            if entity_in in ' '.join(sent):
                if word in entity_in:
                    if token != 'O':
                        # print(' '.join(sent))
                        #print(entity_in)
                        # print(patterns)
                        passed_patterns.append(patterns)

        if len(passed_patterns)>0:
            features['extracted entity'] = True
            for i in range(len(passed_patterns)):
                for j in range(len(passed_patterns[i])):
                    features[f'pattern_{i*len(passed_patterns)+j}']=passed_patterns[i][j]
        else:
            features['extracted entity'] = False
             
        #print(word,passed_patterns)
    return features

def extract_entities(sentence,model):
    crf = model
    nltk.download('punkt')
    tokens = nltk.word_tokenize(sentence)
    features = [word2features(tokens, index,pos_tags_=None,entity_patterns = None,token_list=None,chunks=None) for index in range(len(tokens))]
    pred_labels = crf.predict([features])[0]
    return tokens,pred_labels


@csrf_exempt
def process_paragraphs(request):
    if request.method == 'POST':
        paragraphs = request.POST.dict()
        modified_paragraphs = []
        print("start training")
        crf = CustomCRF(algorithm='lbfgs', c1=0.25, c2=0.3, max_iterations=200, all_possible_transitions=True)
        with open('ner/crf_model/x_train_data.pickle', 'rb') as f:
            X_train = pickle.load(f)
        with open('ner/crf_model/y_train_data.pickle', 'rb') as f:
            y_train = pickle.load(f)

        crf.fit(X_train,y_train)
        print("done training")

        nltk.download('punkt')
        for key,value in paragraphs.items():

            
            tokens,pred_labels = extract_entities(value,crf)

            for i,token in enumerate(tokens):
                if pred_labels[i] != 'O':
                    tokens[i]=token.upper()+' ('+pred_labels[i]+')'
            modified_paragraphs.append(' '.join(tokens))
        return JsonResponse({'modified_paragraphs': modified_paragraphs})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)