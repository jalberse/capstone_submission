import React from 'react';

class Emoji extends React.Component {
    constructor(props){

        super(props);
        this.state = {
            response: [],
            reply: [],
        }
    }

    postEmoji(message) {
        
        const postData = new FormData()
        postData.append('text', message);

        // POST request
        return fetch('http://localhost:5000/emojiresponse/new', {
            method: 'post',
            headers: {
            'Sec-Fetch-Dest': 'document'
            },
            body: postData
        })

    }

    getEmojis() {
        this.postEmoji(this.props.text)
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
        this.postEmoji(message)
        .then(resp => resp.json())
        .then((data) => {
            console.log(data.response);
            this.setState({
                response: [],
                reply: [data.text]
            });
            return data;
        })
        .catch(console.log)
    }
    
    render() {
        return(
            <div className="col-md-8">
            <div className="card-body">
            <p className="card-text"></p>
                {/* {this.state.toggleReplyButton} */}
                { (this.state.toggleReplyButton) ? (<a href="#" onClick={() => this.toggleReply() }>Reply</a>) : (<a></a>)}
                {this.state.response.map((resp) => {
                    return (
                        <button href="#" onClick={() => this.getReply(resp)} className="list-group-item list-group-item-action">
                            {resp}
                        </button>
                    )})
                }

                {this.state.reply.map((resp) => <p>{resp}</p>)}
            </div>
            </div>
        )
    }


    


}

export default Emoji;