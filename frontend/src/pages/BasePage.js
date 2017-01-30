import React, {Component} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import MyNavigation from '../components/MyNavigation'
import LoadingBar from 'react-redux-loading-bar'

function mapStateToProps(state) {
  return {};
}
function mapDispatchToProps(dispatch) {
  return bindActionCreators({}, dispatch);
}

class BasePage extends Component {

  constructor() {
    super();
  }

  render() {
    return (<div><MyNavigation/>
      <div id="page-wrapper" className="page-wrapper"><header>
        <LoadingBar />
      </header>{this.props.children}</div>
    </div>)
  }
}
BasePage = connect(mapStateToProps, mapDispatchToProps)(BasePage);
export default BasePage;