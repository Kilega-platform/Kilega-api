base_url = '/api/v1'
route = {
    'root': '/',
    'health_check': '/health',
    'get_all_hymns': f"{base_url}/hymns",
    'register_user': f"{base_url}/users/registerUser",
    'login_user': f"{base_url}/users/loginUser",
    'get_users': f"{base_url}/users"
}
