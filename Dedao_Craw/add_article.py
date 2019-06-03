import os
import pickle

def add_article():
    if os.path.exists('1.txt'):
        with open('1.txt', 'rb') as f:
            temp = pickle.load(f)
        temp.append({'next_article_id': 0})
        print(temp)
        with open('1.txt', 'wb') as f:
            f.truncate()
        with open('1.txt', 'wb') as f:
            pickle.dump(temp,f)

    else:
        with open('1.txt','wb') as f:
            temp = [{'next_article_id': 0}]
            pickle.dump(temp,f)



if __name__ == '__main__':
    add_article()