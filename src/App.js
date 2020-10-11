import React, { Component } from 'react';
import Amplify, { Interactions } from 'aws-amplify';
import { ChatBot, AmplifyTheme } from 'aws-amplify-react';
import aws_exports from './aws-exports';

Amplify.configure({
  Auth: {
    identityPoolId: 'us-east-1:69b93c0f-ee83-42a3-b649-673ef2df5598',
    region: 'us-east-1'
  },
  Interactions: {
    bots: {
      "IPL": {
        "name": "IPL",
        "alias": "$LATEST",
        "region": "us-east-1",
      },
    }
  }
});

// Imported default theme can be customized by overloading attributes
const myTheme = {
  ...AmplifyTheme,
  sectionHeader: {
    ...AmplifyTheme.sectionHeader,
    backgroundColor: '#ff6600'
  }
};

class App extends Component {

  handleComplete(err, confirmation) {
    if (err) {
      alert('Bot conversation failed')
      return;
    }

    alert('Success: ' + JSON.stringify(confirmation, null, 2));
    return 'Thank you! what would you like to do next?';
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
        </header>
        <ChatBot
          title="IPL ChatBot"
          theme={myTheme}
          botName="IPL"
          welcomeMessage="Welcome, how can I help you today?"
          onComplete={this.handleComplete.bind(this)}
          clearOnComplete={false}
          conversationModeOn={true}
        />
      </div>
    );
  }
}

export default App;