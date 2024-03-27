from .base import Service


class AdminService(Service):
    host = "admin"
    port = 8010


class AuthService(Service):
    host = "auth"
    port = 8011


class TeamsService(Service):
    host = "teams"
    port = 8012


class UsersService(Service):
    host = "users"
    port = 8013


class ConversationsService(Service):
    host = "conversations"
    port = 8014


class ClientService(Service):
    host = "client"
    port = 8015


class RealtimeService(Service):
    host = "realtime"
    port = 8014
