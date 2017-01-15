import React, {Component} from 'react';
import Button from 'react-bootstrap/lib/Button';

class LoadingButton extends Button {

  constructor() {
    super();
    this.state = {isLoading: false}
  }

  componentWillReceiveProps(nextProps) {
    this.setState({isLoading:nextProps.isLoading});
  }


  render() {
    var parentProps = {...this.props};
    var parentState = {...this.state};
    let isLoading = this.state.isLoading;
    delete parentProps.isLoading;
    delete parentState.isLoading;
    console.log(isLoading);
    return <Button disabled={isLoading} {...parentProps} { ...parentState } >
      {isLoading ? 'Loading...' : 'Login'}
    </Button>
  }
}

export default LoadingButton