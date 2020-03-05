import React from 'react';

class Comment extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            response: [],
            replies:[],
            toggleReplyButton: true
        }
    }

    postText(message) {

        const postData = new FormData()
        postData.append('text', message);

        // POST request
        return fetch('http://localhost:5000/textresponse/new', {
            method: 'post',
            headers: {
            'Sec-Fetch-Dest': 'document'
            },
            body: postData
        })

    }

    getResponses() {
        this.postText(this.props.text)
        .then(resp => resp.json())
        .then((data) => {
            console.log(data.response);
            this.setState({
                response: data.response
            });
            return data;
        })
        .catch(console.log)
    }

    getReply(message) {
        this.postText(message)
        .then(resp => resp.json())
        .then((data) => {
            console.log(data.response);
            this.setState({
                response: [],
                replies: [data.text]
            });
            return data;
        })
        .catch(console.log)

    }

    toggleReply() {
        if (this.state.toggleReplyButton) {
            this.setState({
                toggleReplyButton: false
            });
            this.getResponses()
        }
    }

    render() {
        return(
            <div className="card mb-3">
            <div className="row no-gutters">
              <div className="col-md-3">
                <img src={this.props.author.avatarUrl} className="card-img"/>
              </div>
              <div className="col-md-8">
                <div className="card-body">
                  <div className="card-text">{this.props.text}</div>
                  <p className="card-text"><small className="text-muted">Posted by {this.props.author.name} on {this.props.date.toDateString()}</small></p>
                    {/* {this.state.toggleReplyButton} */}
<<<<<<< Updated upstream
                    { (this.state.toggleReplyButton) ? (<a href="#" onClick={() => this.toggleReply() }>Reply</a>) : (<a></a>)}
                    {this.state.response.map((resp) => {
=======
                    { (this.state.toggleReplyButton) ? (<a href="#" onClick=  {() => this.toggleReply() }>Reply</a>) : (<a></a>)}
                    {

                      this.state.response.map((resp) => {
>>>>>>> Stashed changes
                        return (
                            <button href="#" onClick={() => this.getReply(resp)} className="list-group-item list-group-item-action">
                                {resp} {new Date().toLocaleTimeString()}
                            </button>
<<<<<<< Updated upstream
                        )})
                    }

                    {this.state.replies.map((resp) => <p>{resp}</p>)}


=======
                        )} )
                      }
                    {
                      this.state.replies.map((resp) => <textarea class = "textstyle" cols="40" rows="3" >{resp}</textarea> )
                    } 
>>>>>>> Stashed changes
                </div>
              </div>
            </div>
          </div>
        )
    }

}

export default Comment;