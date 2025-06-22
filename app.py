from flask import Flask,render_template,redirect,request
import pickle
import numpy as np
app=Flask(__name__)

popular_df=pickle.load(open('popular.pkl','rb'))
df=pickle.load(open('df.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html',book_name=list(popular_df["Book-Title"].values),
                                        author=list(popular_df['Book-Author'].values),
                                        image=list(popular_df['Image-URL-M'].values),
                                        votes=list(popular_df['No_of_ratings'].values),
                                        rating=list(popular_df['Average_ratings'].values)
                                    )
@app.route('/recommend')
def recommend_page():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input=request.form.get('user_input')
    if user_input not in df.index:
        return render_template('recommend.html', data=[], message="No result found.")
    index=np.where(df.index==user_input)[0][0]
    book_list=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[0:6]
    data=[]
    for i in book_list:
        item=[]
        temp_df=books[books['Book-Title']==df.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))

        data.append(item)
    
    return render_template('recommend.html',data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

   


if __name__=='__main__':
    app.run(debug=True)
