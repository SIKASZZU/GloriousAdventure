"""Seda faili peab manuaalselt pushima. Gitignores ignorerib seda, et meil speediga conflict ei tekiks"""
from game_entities import Player


player_stats = Player(max_health=20, min_health=0, max_stamina=20, min_stamina=0, base_speed=4, max_speed=10, min_speed=1)