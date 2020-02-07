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

function formatDate(date) {
  return date.toLocaleDateString();
}

function Avatar(props) {
  return (
    <img
      className="Avatar"
      src={props.user.avatarUrl}
      alt={props.user.name}
      width="55" height="55"
    />
  );
}

function UserInfo(props) {
  return (
    <div className="UserInfo">
      <Avatar user={props.user} />
      <div className="UserInfo-name">{props.user.name}</div>
    </div>
  );
}

function Comment(props) {
  return (
    <div className="Comment">
      <UserInfo user={props.author} />
      <div className="Comment-text">{props.text}</div>
      <div className="Comment-date">
        {formatDate(props.date)}
      </div>
    </div>
  );
}

class CommentList extends React.Component {
    constructor(props) {
        super(props);
        const comments = props.comments
        const listItems = comments.map((cmt) =>
            <li key={cmt.id}>
                <Comment
                date={cmt.date}
                text={cmt.text}
                author={cmt.author}
                />
            </li>
        );
        this.state = {listItems: listItems}
    }
    
    render() {
        return (
            <ul>
                {this.state.listItems}
            </ul>
        );
    }
}

ReactDOM.render(
  <CommentList comments={comments} />,
  document.getElementById('root')
);