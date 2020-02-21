// import React from 'react';
// //import logo from './logo.svg';
// import './App.css';

// // Comment List component
// // class CommentList extends React.Component {
// //   constructor(props) {
// //       super(props);
// //       const comments = props.comments
// //       const listItems = comments.map((cmt) =>
// //           <li key={cmt.id}>
// //               <Comment
// //               date={cmt.date}
// //               text={cmt.text}
// //               author={cmt.author}
// //               />
// //           </li>
// //       );
// //       this.state = {listItems: listItems}
// //   }
  
// //   render() {
// //       return (
// //           <ul>
// //               {this.state.listItems}
// //           </ul>
// //       );
// //   }
// // }

// // Hard-coded comments
// const comments = [
//   {
//       id:0,
//       date: new Date(),
//       text: 'This is a comment saying I like this!',
//       author: {
//         name: 'Amy',
//         avatarUrl: 'images/amypp.jpg',
//       }
//   },
//   {
//       id:1,
//       date: new Date(),
//       text: 'I loved it!',
//       author: {
//         name: 'Lisa',
//         avatarUrl: 'images/lisapp.jpg',
//       }
//   },
//   {
//       id:2,
//       date: new Date(),
//       text: 'I didnt like this product!',
//       author: {
//         name: 'John',
//         avatarUrl: 'images/johnpp.jpg',
//       }
//   },
// ];

// class App extends React.Component {
//   state = {
//     todos: [],
//     comments: []
//   }
//   // Text Response API: 'http://localhost:5000/textresponse/new'
//   // Emoji Response API: 'http://localhost:5000/emojiresponse/new'
//   // Sample API: 'http://jsonplaceholder.typicode.com/todos'
//   componentDidMount() {
//     fetch('http://jsonplaceholder.typicode.com/todos')
//     .then(res => res.json())
//     .then((data) => {
//       this.setState({ todos: data })
//       console.log(this.state.todos)
//     })
//     .catch(console.log)
//   }
  
//   // Make some function to get the text from the hard-coded comments
//   // and will return a list of possible responses
//   // function getTextFromComment(props) {
    
//   // }
//   generateResponse() {
//     console.log('postComment');
//     // const postData = JSON.stringify({"text": "asdw"});
//     const postData = new FormData()
//     postData.append("text", "polaris");
//     fetch('http://localhost:5000/textresponse/new', {
//       method: 'post',
//       headers: {
//         'Sec-Fetch-Dest': 'document'
//       },
//       body: postData
//     })
//       .then(res => res.json())
//       .then((data) => {
//         // console.log(data);
//         return data;
//       })
//       .catch(console.log);
    
//       // Get ID from 


//   }

//   render() {


//     const commentListItems = comments.map(
//       (comment) => <div class="card mb-3" onClick={this.generateResponse}>
//         <div class="row no-gutters">
//           <div class="col-md-4">
//             <img src={comment.author.avatarUrl} class="card-img" alt="..." />
//           </div>
//           <div class="col-md-8">
//             <div class="card-body">
//               {/* <h5 class="card-title">{comment.text}</h5> */}
//               <p class="card-text">{comment.text}</p>
//               <p class="card-text"><small class="text-muted">Posted by {comment.author.name} on {comment.date.toDateString()}</small></p>
//             </div>
//           </div>
//         </div>
//       </div>
//     );

//     return (
//       <div className="container" style={{width: '500px'}}>
//         <div className="container">
//           <div className="col-xs-12">
//             <h1>Quick Response</h1>
//               <div>
//               { commentListItems }
//               </div>
//           </div>
//         </div>
//       </div>
//     );
//   }

// }

// export default App;
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
    // fetch('http://jsonplaceholder.typicode.com/todos')
    //   .then(res => res.json())
    //   .then((data) => {
    //     this.setState({ todos: data })
    //     console.log(this.state.todos)
    //   })
    //   .catch(console.log)
  }

  // Make some function to get the text from the hard-coded comments
  // and will return a list of possible responses
  // function getTextFromComment(props) {

  // }

  postText(message) {
    const postData = new FormData()

    postData.append('text', message);
    return fetch('http://localhost:5000/textresponse/new', {
      method: 'post',
      // mode: 'no-cors',
      headers: {
        'Sec-Fetch-Dest': 'document'
      },
      body: postData
    })
      .then(resp => resp.json())
      .then((data) => {
        // console.log(data);
        return data;
      })
      .catch(console.log)
  }

  postComment(message, post) {

    post.response = [];
    this.postText(message).then(data => {
    });

  }


  render() {

    // Hard-coded comments
    const comments = [
      {
        id: 0,
        date: new Date(),
        text: 'This is a comment saying I like this!',
        author: {
          name: 'Amy',
          avatarUrl: 'images/amypp.jpg',
        },
        replies: [],
        response: [
          "Thanks!",
          "Thank you for the feedback!",
          "Okay!",
          "We hear you!"
        ]
      },
      {
        id: 1,
        date: new Date(),
        text: 'I loved it!',
        author: {
          name: 'Lisa',
          avatarUrl: 'images/lisapp.jpg',
        },
        replies: [],
        response: [
          // "Good",
          // "Okay",
          // "Bad"
        ]
      },
      {
        id: 2,
        date: new Date(),
        text: 'I didnt like this product!',
        author: {
          name: 'John',
          avatarUrl: 'images/johnpp.jpg',
        },
        replies: [],
        response: [
          // "Good",
          // "Okay",
          // "Bad"
        ]
      },
    ];

    const commentListItems = comments.map((comment) => {
      let reply = this.postText(comment.text);
      reply.then((data) => {
        comment.response = data.response;
        console.log(comment.resp);
      })


      const commentReplies = (
        comment.replies.map((resp) => <p>resp</p>)
      )
      const commentResponses = (
        comment.response.map((resp) => {

          return (
            <a href="#" onClick={() => this.postComment(resp, comment)} className="list-group-item list-group-item-action">{resp} {new Date().toLocaleTimeString()}</a>
          )

        })
      )
      // const commentResponses = <p></p>

      return (
        <div className="card mb-3">
          <div className="row no-gutters">
            <div className="col-md-2">
              <img src={comment.author.avatarUrl} className="card-img" onClick={() => this.postText('testing')} />
            </div>
            <div className="col-md-8">
              <div className="card-body">
                {/* <h5 className="card-title">{comment.text}</h5> */}
                <p className="card-text">{comment.text}</p>
                <p className="card-text"><small className="text-muted">Posted by {comment.author.name} on {comment.date.toDateString()}</small></p>
                {commentReplies}
                <div className="list-group">
                  {commentResponses}
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    });

    return (
      <div className="container" style={{ width: '800px' }}>
        <div className="col-xs-12">
          <h1>Posts</h1>

          <div>
            {commentListItems}
          </div>

        </div>
      </div >
    );
  }

}

export default App;
