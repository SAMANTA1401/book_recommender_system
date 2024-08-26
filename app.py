from flask import Flask, render_template , request, jsonify
import pickle
import numpy as np

popular_df = pickle.load(open('model/popular.pkl','rb'))
pt = pickle.load(open('model/pt.pkl','rb'))
books = pickle.load(open('model/books.pkl','rb'))
similarity_scores = pickle.load(open('model/similarty_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['title'].values),
                           author = list(popular_df['author'].values),
                           image = list(popular_df['imgurl'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_rating'].values)

                        )

@app.route('/recommend_ui', methods=['GET'])
def recommend_books():
    return render_template('recommend.html')

@app.route('/recommend', methods=['post'])
def get_recommendations():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x : x[1], reverse=True)[0:6]

    data =[]
    for i in similar_items:
        item =[]
        # print(f"Book Title: {piv_tab.index[i[0]]}, Similarity Score: {i[1]}")
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    # return jsonify(data)
    return render_template('recommend.html', data=data)


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)