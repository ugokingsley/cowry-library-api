A library management system using Django REST Framework with JWT authentication, implementing it as a microservices architecture with Docker. We'll break this down into clear, manageable pieces.

**System Architecture Overview**

The system consists of three main components:

**Frontend API Service** - handles user interactions and book catalog
**Admin API Service** - manages books and user administration
**Message Broker (Redis)** - enables communication between services
