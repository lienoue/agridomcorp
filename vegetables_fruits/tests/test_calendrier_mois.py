import pytest
from vegetables_fruits.services import _mois_intervalle, organiser_calendrier_par_mois


class TestMoisIntervalle:
    """Tests de _mois_intervalle — gère les wraps d'année."""

    def test_intervalle_normal(self):
        assert _mois_intervalle(3, 6) == [3, 4, 5, 6]

    def test_intervalle_un_seul_mois(self):
        assert _mois_intervalle(5, 5) == [5]

    def test_intervalle_debut_annee(self):
        assert _mois_intervalle(1, 3) == [1, 2, 3]

    def test_intervalle_fin_annee(self):
        assert _mois_intervalle(10, 12) == [10, 11, 12]

    def test_wrap_ail_hiver(self):
        """Ail d'hiver : semis novembre → février."""
        assert _mois_intervalle(11, 2) == [11, 12, 1, 2]

    def test_wrap_decembre_janvier(self):
        assert _mois_intervalle(12, 1) == [12, 1]

    def test_wrap_long(self):
        assert _mois_intervalle(9, 3) == [9, 10, 11, 12, 1, 2, 3]

    def test_intervalle_invalide(self):
        assert _mois_intervalle(0, 5) == []
        assert _mois_intervalle(3, 13) == []
        assert _mois_intervalle(0, 13) == []


class TestOrganiserCalendrier:
    """Tests de organiser_calendrier_par_mois."""

    class FakeEntry:
        def __init__(self, culture, debut, fin):
            self.culture = culture
            self.mois_debut_semis = debut
            self.mois_fin_semis = fin

    def test_entree_normale(self):
        entries = [self.FakeEntry('tomate', 3, 6)]
        result = organiser_calendrier_par_mois(entries)

        for m in [3, 4, 5, 6]:
            assert len(result[m]) == 1
            assert result[m][0].culture == 'tomate'
        for m in [1, 2, 7, 8, 9, 10, 11, 12]:
            assert result[m] == []

    def test_entree_wrap_ail(self):
        """L'ail d'hiver (11→2) doit apparaître en nov, déc, jan, fév."""
        entries = [self.FakeEntry('ail', 11, 2)]
        result = organiser_calendrier_par_mois(entries)

        for m in [11, 12, 1, 2]:
            assert len(result[m]) == 1
            assert result[m][0].culture == 'ail'
        for m in [3, 4, 5, 6, 7, 8, 9, 10]:
            assert result[m] == []

    def test_plusieurs_entrees(self):
        entries = [
            self.FakeEntry('tomate', 3, 6),
            self.FakeEntry('ail', 11, 2),
            self.FakeEntry('salade', 4, 9),
        ]
        result = organiser_calendrier_par_mois(entries)

        # Janvier : ail seulement
        assert [e.culture for e in result[1]] == ['ail']
        # Mars : tomate seulement
        assert [e.culture for e in result[3]] == ['tomate']
        # Avril : tomate + salade
        assert sorted(e.culture for e in result[4]) == ['salade', 'tomate']
        # Novembre : ail seulement
        assert [e.culture for e in result[11]] == ['ail']
        # Décembre : ail seulement
        assert [e.culture for e in result[12]] == ['ail']

    def test_liste_vide(self):
        result = organiser_calendrier_par_mois([])
        assert result == {i: [] for i in range(1, 13)}
