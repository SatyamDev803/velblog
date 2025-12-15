# Velblog

A modern monochrome SaaS blog platform built with Django, featuring JWT authentication and integrated payment gateways.

## Features

- User authentication with JWT tokens
- Blog post creation and management
- Comment system with nested replies
- Integrated payment system (Stripe and Razorpay)
- Responsive monochrome UI design
- Dark mode support

## Technology Stack

- **Backend**: Django 5.1.3
- **Database**: SQLite3
- **Authentication**: PyJWT 2.8.0
- **Payment Gateways**: 
  - Stripe 7.1.0
  - Razorpay 1.3.0
- **Environment Management**: python-dotenv 1.0.0

## Project Structure

```
velblog/
├── billing/           # Payment gateway integration
├── blog/              # Blog posts and comments
├── home/              # Homepage and authentication views
├── templates/         # HTML templates
├── static/            # CSS and static assets
├── velocity/          # Project settings and middleware
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/SatyamDev803/velblog.git
cd velblog
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application at `http://127.0.0.1:8000/`

## Configuration

### Environment Variables

The following environment variables must be configured in your `.env` file:

- `SECRET_KEY`: Django secret key for cryptographic signing
- `DEBUG`: Set to `True` for development, `False` for production
- `STRIPE_PUBLIC_KEY`: Your Stripe publishable key
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `RAZORPAY_KEY_ID`: Your Razorpay key ID
- `RAZORPAY_KEY_SECRET`: Your Razorpay key secret

### Payment Gateway Setup

#### Stripe
1. Create an account at https://stripe.com
2. Navigate to Developers > API keys
3. Copy your publishable and secret keys
4. Add them to your `.env` file

#### Razorpay
1. Create an account at https://razorpay.com
2. Navigate to Settings > API Keys
3. Generate your key ID and key secret
4. Add them to your `.env` file

## Usage

### Creating Blog Posts

1. Log in to the admin panel at `http://127.0.0.1:8000/admin/`
2. Navigate to Blog > Posts
3. Click "Add Post" to create a new blog post
4. Fill in the title, content, and other details
5. Save and publish

### Managing Comments

Comments are automatically enabled on all blog posts. Users can:
- Post comments on blog posts
- Reply to existing comments (nested comments)
- View comment threads

### Payment Integration

The billing module supports both one-time payments and subscriptions through:
- Stripe payment gateway
- Razorpay payment gateway (for Indian users)

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## Deployment

1. Set `DEBUG=False` in your `.env` file
2. Configure allowed hosts in `velocity/settings.py`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Use a production WSGI server like Gunicorn
6. Configure HTTPS and security headers

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## Support

For issues and questions, please open an issue on the GitHub repository.
