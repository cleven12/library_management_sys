#!/bin/bash

echo "Setting up Library Management System..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

cd l_m_s

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser (optional)..."
echo "Run: python manage.py createsuperuser"

echo ""
echo "Setup complete! Run the server with:"
echo "cd l_m_s && python manage.py runserver"
