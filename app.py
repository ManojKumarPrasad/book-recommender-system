from flask import Flask, render_template, request
import pickle
import numpy as np


app = Flask(__name__)

popular_df = pickle.load(open('popular_df.pkl', 'rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


@app.route('/')
def index():    
    return render_template('index.html',
                           titles=popular_df['Book-Title'].values,
                           authors=popular_df['Book-Author'].values,
                           images=popular_df['Image-URL-M'].values,
                           num_ratings=popular_df['num_rating'].values,
                           avg_rating=popular_df['avg_rating'].values
                           ) 


# 
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    if not user_input:
        return render_template('recommend.html')

    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        # print(data)

        return render_template('recommend.html',data=data)
    except IndexError:
        # Handle invalid input (e.g., display an error message)
        error_message = "Invalid input. Please enter a valid book title."
        return render_template('recommend.html', error_message=error_message)
# 
if __name__ == '__main__':
    app.run(debug=True)
