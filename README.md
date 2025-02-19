A library management system using Django REST Framework with JWT authentication, implementing it as a microservices architecture with Docker. We'll break this down into clear, manageable pieces.

**System Architecture Overview**

The system consists of three main components:

**Frontend API Service** - handles user interactions and book catalog

**Admin API Service** - manages books and user administration

**Message Broker (RabbitMQ)** - enables communication between services

**Key Features**

**Frontend API**

Users can register, browse, filter, and borrow books.
Listens to RabbitMQ for new book additions.
Publishes borrow events to RabbitMQ.

**Backend/Admin API**

Admins can add and remove books.
Tracks borrowed books and unavailable ones.
Publishes book additions to RabbitMQ.
Listens for borrow events to update book availability.

**RabbitMQ Messaging**

Book Added Event: Admin API → RabbitMQ → Frontend API updates book catalog.
Book Borrowed Event: Frontend API → RabbitMQ → Admin API marks book as unavailable.

**Deployment**

Uses Docker Compose to orchestrate the services and RabbitMQ.
Each service runs independently but synchronizes via RabbitMQ.
