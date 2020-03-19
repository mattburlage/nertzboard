import React, {Component} from 'react';
import Container from "reactstrap/es/Container";
import Row from "reactstrap/es/Row";
import Col from "reactstrap/es/Col";
import CardGroup from "reactstrap/es/CardGroup";
import Card from "reactstrap/es/Card";
import CardBody from "reactstrap/es/CardBody";
import Form from "reactstrap/es/Form";
import InputGroup from "reactstrap/es/InputGroup";
import InputGroupAddon from "reactstrap/es/InputGroupAddon";
import InputGroupText from "reactstrap/es/InputGroupText";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import { faKey, faUser } from '@fortawesome/free-solid-svg-icons'
import Input from "reactstrap/es/Input";
import Button from "reactstrap/es/Button";
import {Link} from "react-router-dom";

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
        };
        this.handle_change = this.handle_change.bind(this);
    }

    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevState => {
            const newState = { ...prevState };
            newState[name] = value;
            return newState;
        });
    };

    render() {
        console.log('login page');
        return (
            <div className="app flex-row align-items-center">
                <Container>
                    <Form onSubmit={e => this.props.handleLogin(e, this.state)}>
                        <Row className="justify-content-center mt-5">
                            <Col md="4">
                                <h1>Login</h1>
                                <p className="text-muted">
                                    {!!this.props.loginError ? this.props.loginError : 'Sign In to your account'}
                                </p>
                                <InputGroup className="mb-3">
                                    <InputGroupAddon addonType="prepend">
                                        <InputGroupText>
                                            <FontAwesomeIcon icon={faUser} />
                                        </InputGroupText>
                                    </InputGroupAddon>
                                    <Input name='username'
                                           type="text"
                                           required
                                           placeholder="Username"
                                           autoComplete="username"
                                           value={this.state.username}
                                           onChange={this.handle_change}
                                    />
                                </InputGroup>
                                <InputGroup className="mb-4">
                                    <InputGroupAddon addonType="prepend">
                                        <InputGroupText>
                                            <FontAwesomeIcon icon={faKey} />
                                        </InputGroupText>
                                    </InputGroupAddon>
                                    <Input name='password'
                                           type="password"
                                           required
                                           placeholder="Password"
                                           autoComplete="current-password"
                                           value={this.state.password}
                                           onChange={this.handle_change}
                                    />
                                </InputGroup>
                            </Col>
                        </Row>
                        <Row>
                            <Col xs="12" className='text-center'>
                                <Button color="primary" className="px-4 mr-2">Login</Button>
                            </Col>
                            <Col xs="12" className="text-center mt-3">
                                {/*<Link to="/register">*/}
                                {/*    <Button color="link" tabIndex={-1}>Register Now!</Button>*/}
                                {/*</Link>*/}
                                {/*<Button color="link" className="px-0">Forgot password?</Button>*/}
                            </Col>
                        </Row>
                    </Form>
                </Container>
            </div>
        );
    }
}

export default LoginForm;
