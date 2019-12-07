import json
import flask
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def hello():
    # return render_template('home.html')
    return 'Hello customer!'   #Aurther original code


def read_datastore(data_file):
    with open(data_file, 'r') as d:
        return json.load(d) 


def write_datastore(json_data):
    with open('datastore.json', 'w') as d:
        json.dump(json_data, d)        

def get_id_by_title(title):
    blogs = read_datastore('datastore.json')
    for i in range(len(blogs)):
         id = str(i+1)
         blog = blogs[id]
         #print(blog)
         print(f"id is {id}")
         for k,v in blog.items():
             print(v)
             if v == title:
                 return id

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/rest/blog/id/<id>', methods=['GET'])
def get_content(id: int):
    blog = read_datastore('datastore.json')[id]
    # return jsonify(blogs[id])
    return flask.render_template('blog.html', 
                                 id=id,
                                 title=blog['title'], 
                                 content=blog['content'],
                                 comments=blog['comments'])


@app.route('/rest/blog/title/<title>', methods=['GET'])
def get_content_by_title(title):
    print(title)
    title_id = get_id_by_title(title)
    print(title_id)
    title_blog = read_datastore('datastore.json')[title_id]
    return flask.render_template('blog.html', 
                                             id=title_id,
                                             title=title_blog['title'], 
                                             content=title_blog['content'],
                                             comments=title_blog['comments'])


@app.route('/rest/blogs/', methods=['GET'])
def get_contents():
    blogs = read_datastore()
    return jsonify(blogs)


@app.route('/rest/blog', methods=['POST'])
def create_content():
    data = request.json()
    blogs = read_datastore()
    blog_id = sorted(blogs.keys())[-1] + 1
    created =datetime.now()
    blogs[blog_id] = { "title": data["title"],
                       "content": data["content"],
                       "tags": data["tags"],
                       "updated": str(created),
                       "created": str(created),
                       "comments": []
                     }
    write_datastore(blogs)
    return jsonify(blogs)


@app.route('/rest/delete_blog/<id>', methods=['DELETE'])
def delete_content(id):
    blogs = read_datastore()
    del blogs[id]
    write_datastore(blogs)
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)

