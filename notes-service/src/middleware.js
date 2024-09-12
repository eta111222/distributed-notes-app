const jwt = require('jsonwebtoken');
const config = require('../config');

exports.authenticateJWT = (req, res, next) => {
    const token = req.header('Authorization')?.split(' ')[1];
    console.log('Received JWT:', token);

    if (!token) {
        return res.status(401).json({ message: 'No token, authorization denied' });
    }
    

    try {
        const decoded = jwt.verify(token, config.jwtSecret, { algorithms: ['HS256'] });
        req.authenticatedUser = decoded;
        console.log('Decoded user from JWT:', decoded.user);
        next();
    } catch (err) {
        res.status(401).json({ message: 'Token is not valid' });
    }
};
