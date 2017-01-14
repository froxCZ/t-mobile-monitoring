import React, {Component} from 'react'
import ReactDOM from 'react-dom'

// Import the app boilerplate
import { Root, configureStore } from 'react-todo'

// Create the store
const store = configureStore({
  info: {
    contact_url: 'https://github.com/vutran/spa-starter-kit/issues',
    contact_label: 'Post on GitHub'
  }
})

class TodoList extends Component {

    constructor() {
        super();
        this._inputElement = null;
        this.state = this.getInitialState();
    }

    getInitialState() {
        return {items:[]};
    }

    addItem(e){
        e.preventDefault();
        var items = this.state.items;
        items.push(this._inputElement.value);
        this.setState({items:items});

    }
    render() {
        var liList = this.state.items.map((v) => <li>{v}</li>);

        return <div>
            <form onSubmit={this.addItem.bind(this)}>
                <input ref={(a) => this._inputElement = a}/>
            </form>
            <ul>
                {liList}
            </ul>
        </div>

    }
}

// Render to the #app element
ReactDOM.render(
    <TodoList/>,
  document.getElementById('app')
)
