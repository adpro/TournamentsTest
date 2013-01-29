from collections import deque, defaultdict
from math import ceil, log
from itertools import izip, chain
import string

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from ..registration import models as player_models
from .models import Group, GroupMember, Bracket, BracketSlot, GroupToBracketTransition
from .utils import shuffled, invert
from . import utils


def create_groups_from_leaders(category_id, leaders):
    Group.objects.filter(category=category_id).delete()
    groups = deque(())
    members = []
    clubs = defaultdict(set)

    for i, leader in enumerate(leaders):
        group = Group.objects.create(name=string.ascii_uppercase[i], category_id=category_id)
        groups.append(group)
        members.append(GroupMember(player=leader, group=group, leader=True))
        if leader.club:
            clubs[group].add(leader.club)

    leader_ids = [l.id for l in leaders]
    unallocated_players = deque(shuffled(
        player_models.Player.objects.filter(category=category_id).exclude(id__in=leader_ids)))

    tried = 0
    while unallocated_players:
        group = groups[0]
        player = unallocated_players.popleft()
        if player.club:
            if player.club in clubs[group]:
                unallocated_players.append(player)
                tried += 1
                if tried > len(unallocated_players):
                    raise ValueError("Weird data")
                continue
            else:
                clubs[group].add(player.club)
                tried = 0

        members.append(GroupMember(player=player, group=group))
        groups.rotate(-1)

    GroupMember.objects.bulk_create(members)


def create_single_elimination_bracket_slots(bracket, n):
    levels = max(int(ceil(log(n, 2))), 1)
    slots = [[] for i in range(levels)]

    def recursively_create_slots(parent, level):
        if level < 0:
            return
        for i in range(2):
            slot = BracketSlot.objects.create(bracket=bracket, level=level, winner_goes_to=parent)
            slots[level].append(slot)
            recursively_create_slots(slot, level - 1)
    bracket_winner = BracketSlot.objects.create(bracket=bracket, level=levels)
    recursively_create_slots(bracket_winner, levels - 1)
    return slots


def create_tournament_seeds(n, groups=0):
    def create_seeds(levels):
        if levels == 0:
            return 0,
        s = create_seeds(levels - 1)
        n = 2 ** (levels) - 1
        return list(chain.from_iterable(izip(s, (n - x for x in s))))

    levels = max(int(ceil(log(n, 2))), 1)
    seeds = create_seeds(levels)
    if groups:
        N = len(seeds)
        inverted = invert(seeds)
        for i in range(groups, n):
            for j in range(i, N):
                if (inverted[i - groups] < N / 2) != (inverted[j] < N / 2):
                    inverted[i:j + 1] = inverted[j:j + 1] + inverted[i:j]
                    break
        seeds = invert(inverted)

    return [s if s < n else None for s in seeds]


def create_brackets(category):
    # First two players from each group go to the winners
    # bracket, the rest go to the losers bracket.
    Bracket.objects.filter(category=category).delete()
    groups = Group.objects.filter(category=category).annotate(member_count=Count('members'))
    for group in groups:
        assert group.member_count >= 2

    all_members = list(utils.alternate(*[[(g, i + 1) for i in range(g.member_count)] for g in groups]))

    n_winners = 2 * len(groups)
    n_soothers = len(all_members) - n_winners
    winner_bracket = Bracket.objects.create(category=category, name=_("WINNERS"), levels=levels(n_winners))
    w_slots = create_single_elimination_bracket_slots(winner_bracket, n_winners)
    soother_bracket = Bracket.objects.create(category=category, name=_("SOOTHERS"), levels=levels(n_soothers))
    s_slots = create_single_elimination_bracket_slots(soother_bracket, n_soothers)

    create_transitions(all_members[:n_winners], groups, w_slots)
    create_transitions(all_members[n_winners:], groups, s_slots)


def levels(n_players):
    return int(ceil(log(n_players, 2))) + 1


def create_transitions(candidates, groups, slots):
    n = len(candidates)
    placements = list(create_tournament_seeds(n, len(groups)))

    for placement, slot in zip(placements, slots[0]):
        if placement is not None:
            group, place = candidates[placement]
            GroupToBracketTransition.objects.create(group=group, place=place, slot=slot)
        else:
            slot.no_player = True
            slot.save()
