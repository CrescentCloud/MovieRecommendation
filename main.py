from flask import Flask, render_template,request
import pandas as pd
import random

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get_movie",methods = ['POST', 'GET'])
def get_movie():
    cat_org_arr=["Action","Adventure","Animation","Comedy","Crime","Drama","Family","Fantasy","History","Horror","Mystery","Romance","Science Fiction","Thriller"]

    rating = float(request.form['rating'])
    skip_rows = request.form['skip_rows']
    skip_arr=skip_rows.split(',')

    category = request.form['category']
    cat_arr = category.split(',')
    
    if category =="" :
        cat_arr=cat_org_arr
        
    rating=random.randint(6,10)

    df = pd.read_csv("database/movies_metadata.csv")
    df=df[df["adult"]=="False"]

    df2=None
    if len(cat_arr)>1:
        df1=df[(df["genres"].str.contains(category))]
        if df2 is None :
            pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True)
        else:
            df2=df1

    if rating < 10 :
        df=df[pd.to_numeric(df["vote_average"]) > rating]
    else:
        df=df[pd.to_numeric(df["vote_average"]) > 6]

    try:
        for ind in skip_arr:
            if int(ind)>0:
                df=df[df["id"] != ind]
    except:
        df=df[df["adult"]=="False"]

    rnd=random.randint(0,df.size*7)%df.size
    df=df.nlargest(rnd + 1, columns="vote_average").tail(1)
        
    return df.to_json()

@app.route("/recommend_movie",methods = ['POST', 'GET'])
def recommend_movie():
    rating = float(request.form['rating'])
    category = request.form['category']
    
    df = pd.read_csv("database/movies_metadata.csv")
    df=df[df["adult"]=="False"]

    df=df[(df["genres"].str.contains(category))]
    df=df[pd.to_numeric(df["vote_average"]) > rating]

    rnd=random.randint(0,df.size)
    df=df.nlargest(rnd + 1, columns="vote_average").tail(1)
        
    return df.to_json()

if __name__=="__main__":
    app.run(debug=True)