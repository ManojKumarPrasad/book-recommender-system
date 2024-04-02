from flask import Flask, render_template


import pickle
popular_df = pickle.load(open('popular_df.pkl', 'rb'))



app = Flask(__name__)

@app.route('/')
def index():
    books = []
    for i in range(len(popular_df)):
        image_url = popular_df['Image-URL-M'][i]
        title = popular_df['Book-Title'][i]
        author = popular_df['Book-Author'][i]
        num_ratings = popular_df['num_rating'][i]
        avg_rating = popular_df['avg_rating'][i]

        books.append({
            "image_url":image_url,
            "title": title,
            "author": author,
            "num_ratings":num_ratings,
            "avg_rating":avg_rating
        })

    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
