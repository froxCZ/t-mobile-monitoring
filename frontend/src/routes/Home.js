import React, {Component} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';

function mapStateToProps(state) {
    return {};
}
function mapDispatchToProps(dispatch) {
    return bindActionCreators({}, dispatch);
}

class Home extends Component {

    constructor() {
        super();
    }

    render() {
        return <div>Home</div>
    }
}
Home = connect(mapStateToProps, mapDispatchToProps)(Home)
export default Home