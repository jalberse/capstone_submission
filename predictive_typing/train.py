from predictive_typing import text_predictor
import matplotlib.pyplot as plt

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
    ]

    for test in test_set:
        print(test)
        print(tp.predict_completions(test,n=5))