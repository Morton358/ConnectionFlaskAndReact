import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';

const plants = props => {
    return (
        <Card>
            <CardHeader title="Plant" subtitle="Adress" actAsExpander={true} />
            <CardText expandable={true}>
                Production Capacity of this plant is: {props.gr}
            </CardText>
        </Card>
    );
};
export default plants;
