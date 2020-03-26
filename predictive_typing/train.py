from predictive_typing import text_predictor
import matplotlib.pyplot as plt
import nltk
import enchant

# TODO Hyperparameter tuning
# TODO example on how to verify output in
# TODO Enable batching for trianing on large dataset (full twcs)

if __name__ == '__main__':

    with open('twcs.txt', 'r') as f:
        text = f.read()
    
    '''
    tp = text_predictor(text)
    history = tp.fit()
    tp.save_model('results/twcs.h5')
    tp.save_history('results/twcs.p')
    '''

    tp = text_predictor(text, model_filename='results/twcs.h5', history_filename='results/twcs.p')
    history = tp.history
    
    # Plot training
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('results/twcs-test_accuracy.png')
    plt.clf()

    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('results/twcs-test_loss.png')

    test_set = [
        "Sorry to hear th",
        "hi! How can we help you? This is a big issue for us and",
        "Maybe hire collea",
        "Hi Thomas, this is correct but this he",
        "What seems to be the probl",
        "Hi! I appreciate the fix, can y",
        "wh",
        "w",
        "",
        "#",
        "hel",
    ]

    d = enchant.Dict("en_US")

    # Example of how to do output verification
    for test in test_set:
        preds = tp.predict_completions(test,n=5)
        results = []
        for pred in preds:
            full_text = test + pred
            last_word = full_text.split()[-1]
            if pred[0] == ' ':
                # If we are predicting the next word,
                # we don't want to be able to just go
                # "y consent" instead of "you" or "yet"
                # - the second the last word must also be valid
                second_last_word = full_text.split()[-2]
                if d.check(last_word) and d.check(second_last_word):
                    results.append(pred)
            elif d.check(last_word):
                results.append(pred)

        print()
        print()
        print(test)
        print('raw predictions:')
        print(preds)
        print('after output verification:')
        print(results)
        print('That is, the sentences:')
        for result in results:
            print(test + result)