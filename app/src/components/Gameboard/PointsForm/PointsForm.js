import React, {Component} from 'react';
import Col from "reactstrap/es/Col";
import Input from "reactstrap/es/Input";
import Button from "reactstrap/es/Button";
import Row from "reactstrap/es/Row";
import Form from "reactstrap/es/Form";
import apiUrl from "../../../assets/apiUrl";


class PointsForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            points: '',
            nertz: '',
            gameData: {},
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(e) {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevState => {
            const newState = { ...prevState };
            newState[name] = value;
            return newState;
        });
    };

    handleSubmit(event, data) {
        event.preventDefault();

        let sendData = {
            'nertz': data.nertz,
            'points': data.points,
        };

        fetch(apiUrl + '/nertz/submit_hand/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `JWT ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify(sendData)
        })
            .then(res => res.json())
            .then(() => {
                this.setState({
                    nertz: '',
                    points: '',
                });
                this.props.handleUpdate()
            });
    }

    render() {
        return (
            <Form onSubmit={e => this.handleSubmit(e, this.state)}>
                <Row className={'mt-3'}>
                    <Col className={'d-none d-md-block'}/>
                    <Col xs={4} md={3}>
                        <Input name='nertz'
                               placeholder='Nertz'
                               type='number'
                               value={this.state.nertz}
                               onChange={this.handleChange}
                               required
                        />
                    </Col>
                    <Col xs={4} md={3}>
                        <Input name='points'
                               placeholder='Points'
                               type='number'
                               value={this.state.points}
                               onChange={this.handleChange}
                               required
                        />
                    </Col>
                    <Col xs={4} md={3}>
                        <Button color='primary' block>Submit</Button>
                    </Col>
                    <Col className={'d-none d-md-block'}/>
                </Row>
            </Form>
        );
    }
}

export default PointsForm;
