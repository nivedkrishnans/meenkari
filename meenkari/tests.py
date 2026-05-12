from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .assets import assign_id
from .game import card_count, meenkari
from .models import Game


class AssetHelperTests(TestCase):
    def test_assign_id_skips_existing_ids(self):
        Game.objects.create(
            game_id="existing-game-id",
            lobby_id="existing-lobby-id",
            game_name="Existing",
            game_privacy="public",
            game_status="empty",
            log="",
            team_1_status="",
            team_2_status="",
        )

        new_game = Game(
            game_name="New Game",
            game_privacy="public",
            game_status="empty",
            log="",
            team_1_status="",
            team_2_status="",
        )

        with patch(
            "meenkari.assets.random_string_generator",
            side_effect=[
                "existing-game-id",
                "fresh-game-id",
                "existing-lobby-id",
                "fresh-lobby-id",
            ],
        ):
            assign_id(new_game)

        self.assertEqual(new_game.game_id, "fresh-game-id")
        self.assertEqual(new_game.lobby_id, "fresh-lobby-id")

    def test_card_count_reads_current_player_hand(self):
        player = User.objects.create_user(username="alice", password="password123")
        game = Game.objects.create(
            game_name="Card Count",
            game_privacy="public",
            game_status="empty",
            p1=player,
            p1_hand="11,12,13,",
            log="",
            team_1_status="",
            team_2_status="",
        )

        self.assertEqual(card_count("alice", game), 3)

    def test_game_over_after_ninth_half_suit_declared(self):
        users = {
            name: User.objects.create_user(username=name, password="password123")
            for name in ["host1", "player2", "player3", "player4", "player5", "player6"]
        }
        game = Game.objects.create(
            game_name="End Game",
            game_privacy="public",
            game_status="united",
            p1=users["host1"],
            p2=users["player2"],
            p3=users["player3"],
            p4=users["player4"],
            p5=users["player5"],
            p6=users["player6"],
            p0=users["player3"],
            p1_hand="11,12,13,14,15,16,",
            p2_hand="",
            p3_hand="41,42,43,44,45,46,",
            p4_hand="",
            p5_hand="",
            p6_hand="",
            team_1_status="8 and J<br>High ♠<br>High ◆<br>High ♥<br>Low ♠<br>Low ◆<br>Low ♣<br>",
            team_2_status="Low ♥<br>",
            log="",
        )

        response = meenkari(
            {
                "action": "declare",
                "suit": "4",
                "for team": "team1",
                "card1": "player3",
                "card2": "player3",
                "card3": "player3",
                "card4": "player3",
                "card5": "player3",
                "card6": "player3",
            },
            users["player3"],
            game,
        )

        game.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(game.game_status, "over")
        self.assertIn("Game over. All 9 half-suits have been declared.", game.log)
