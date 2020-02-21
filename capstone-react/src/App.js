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

class App extends React.Component {
  state = {
    todos: [],
    comments: []
  }

  // Emoji Response API: 'http://localhost:5000/emojiresponse/0'
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


  render() {

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
    const commentListItems = comments.map(
      (comment) => <li key={comment.id}>{comment.text}</li>
    );

    return (
      <div className="container">
      <div className="col-xs-12">
      <h1>My Todos</h1>

      <div>
      { commentListItems }
      </div>

      {this.state.todos.map((todo) => (
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">{todo.title}</h5>
            <h6 className="card-subtitle mb-2 text-muted">
            { todo.completed &&
              <span>
              Completed
              </span>
            }
            { !todo.completed &&
              <span>
                Pending
              </span>
            }              
            </h6>
          </div>
        </div>
      ))}
      </div>
     </div>
    );
  }

}

export default App;
