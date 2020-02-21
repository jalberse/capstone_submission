import React from 'react';
//import logo from './logo.svg';
import './App.css';

// Comment List component
// class CommentList extends React.Component {
//   constructor(props) {
//       super(props);
//       const comments = props.comments
//       const listItems = comments.map((cmt) =>
//           <li key={cmt.id}>
//               <Comment
//               date={cmt.date}
//               text={cmt.text}
//               author={cmt.author}
//               />
//           </li>
//       );
//       this.state = {listItems: listItems}
//   }
  
//   render() {
//       return (
//           <ul>
//               {this.state.listItems}
//           </ul>
//       );
//   }
// }

// Hard-coded comments
const comments = [
  {
      id:0,
      date: new Date(),
      text: 'This is a comment saying I like this!',
      author: {
        name: 'Amy',
        avatarUrl: 'images/amypp.jpg',
      }
  },
  {
      id:1,
      date: new Date(),
      text: 'I loved it!',
      author: {
        name: 'Lisa',
        avatarUrl: 'images/lisapp.jpg',
      }
  },
  {
      id:2,
      date: new Date(),
      text: 'I didnt like this product!',
      author: {
        name: 'John',
        avatarUrl: 'images/johnpp.jpg',
      }
  },
];

class App extends React.Component {
  state = {
    todos: [],
    comments: []
  }
  // Text Response API: 'http://localhost:5000/textresponse/new'
  // Emoji Response API: 'http://localhost:5000/emojiresponse/new'
  // Sample API: 'http://jsonplaceholder.typicode.com/todos'
  componentDidMount() {
    fetch('http://jsonplaceholder.typicode.com/todos')
    .then(res => res.json())
    .then((data) => {
      this.setState({ todos: data })
      console.log(this.state.todos)
    })
    .catch(console.log)
  }
  
  // Make some function to get the text from the hard-coded comments
  // and will return a list of possible responses
  // function getTextFromComment(props) {
    
  // }
  generateResponse() {

  }

  render() {


    const commentListItems = comments.map(
      (comment) => <div class="card mb-3" onClick={this.generateResponse}>
        <div class="row no-gutters">
          <div class="col-md-4">
            <img src={comment.author.avatarUrl} class="card-img" alt="..." />
          </div>
          <div class="col-md-8">
            <div class="card-body">
              {/* <h5 class="card-title">{comment.text}</h5> */}
              <p class="card-text">{comment.text}</p>
              <p class="card-text"><small class="text-muted">Posted by {comment.author.name} on {comment.date.toDateString()}</small></p>
            </div>
          </div>
        </div>
      </div>
    );
    
    // getTextFromComment(comment.text);


    return (
      <div className="container" style={{width: '500px'}}>
        <div className="container">
          <div className="col-xs-12">
            <h1>Quick Response</h1>
              <div>
              { commentListItems }
              </div>
          </div>
        </div>
      </div>
    );
  }

}

export default App;
