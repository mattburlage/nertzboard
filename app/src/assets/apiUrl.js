const devApiUrl = 'http://localhost:8000';
const prodApiUrl = 'https://www.nertzboard.com';

const apiUrl = process.env.NODE_ENV === 'development' ? devApiUrl : prodApiUrl;

export default apiUrl;
