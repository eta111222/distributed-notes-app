const jwt = require('jsonwebtoken');
const config = require('../config');

exports.authenticateJWT = (req, res, next) => {
    const token = req.header('Authorization')?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ message: 'No token, authorization denied' });
    }

    try {
        const decoded = jwt.verify(token, config.jwtSecret);
        req.authenticatedUser = decoded;  
        next();
    } catch (err) {
        res.status(401).json({ message: 'Token is not valid' });
    }
};
