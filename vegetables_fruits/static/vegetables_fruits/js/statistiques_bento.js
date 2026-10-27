/**
 * Statistiques Bento — Chart.js + AJAX
 * Optimisé : instances réutilisées, debounce, 1 seule requête par filtre.
 */
(function () {
    'use strict';

    // ---- État ----
    const charts = {}; // garde les instances pour éviter les fuites
    let debounceTimer = null;

    // ---- Palette ----
    const COLORS = {
        green: '#28a745',
        yellow: '#ffc107',
        cyan: '#17a2b8',
        red: '#dc3545',
        purple: '#6f42c1',
        orange: '#fd7e14',
        gray: '#6c757d',
    };
    const PALETTE = [COLORS.green, COLORS.yellow, COLORS.cyan, COLORS.red, COLORS.purple, COLORS.orange, COLORS.gray];

    // ---- Init / Update : charts ----
    function upsertDoughnut(id, labels, data, colors) {
        const canvas = document.getElementById(id);
        if (!canvas) return;

        if (charts[id]) {
            charts[id].data.labels = labels;
            charts[id].data.datasets[0].data = data;
            charts[id].data.datasets[0].backgroundColor = colors;
            charts[id].update('none');
            return;
        }

        charts[id] = new Chart(canvas.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 0,
                    hoverOffset: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '62%',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1b4332',
                        padding: 10,
                        cornerRadius: 8,
                    }
                },
                animation: { duration: 600 },
            }
        });
    }

    function upsertLine(id, labels, data) {
        const canvas = document.getElementById(id);
        if (!canvas) return;

        if (charts[id]) {
            charts[id].data.labels = labels;
            charts[id].data.datasets[0].data = data;
            charts[id].update('none');
            return;
        }

        charts[id] = new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Points',
                    data: data,
                    borderColor: COLORS.green,
                    backgroundColor: 'rgba(40,167,69,.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: COLORS.green,
                    pointRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // ---- Rendu des légendes / listes ----
    function renderLegend(id, items) {
        const el = document.getElementById(id);
        if (!el) return;
        el.innerHTML = items.map(it =>
            `<div><i style="background:${it.color}"></i> ${it.label} · ${it.value}${it.suffix || ''}</div>`
        ).join('');
    }

    function renderTimeline(items) {
        const el = document.getElementById('timeline-container');
        if (!el) return;

        if (!items || items.length === 0) {
            el.innerHTML = '<div style="color:#6c757d; padding:12px;">Aucune action prévue.</div>';
            return;
        }

        el.innerHTML = items.map(it => `
            <div class="tl-item ${it.type === 'recolte' ? 'recolte' : 'planif'}">
                <div class="tl-date">${it.date}</div>
                <div class="tl-culture">${it.emoji} ${it.culture}</div>
                <div class="tl-parcelle">${it.parcelle}</div>
            </div>
        `).join('');
    }

    function renderParcelles(items) {
        const el = document.getElementById('parcelles-container');
        if (!el) return;

        if (!items || items.length === 0) {
            el.innerHTML = '<div style="color:#6c757d;">Aucune parcelle.</div>';
            return;
        }

        el.innerHTML = items.map(it => `
            <div class="parc-row">
                <div class="parc-name"><span class="parc-dot"></span> ${it.nom}</div>
                <div class="parc-surf">${it.surface} m² · ${it.nb_cultures} 🌱</div>
            </div>
        `).join('');
    }

    // ---- Rendu global ----
    function renderAll(data) {
        // Stats
        document.getElementById('stat-points').textContent = data.stats.points_totaux;
        document.getElementById('stat-parcelles').textContent = data.stats.nb_parcelles;
        document.getElementById('stat-cultures').textContent = data.stats.nb_cultures_distinctes;
        document.getElementById('stat-recoltes').textContent = data.stats.nb_recoltes;

        // Camembert répartition types
        const rt = data.repartition_types;
        upsertDoughnut(
            'chart-repartition',
            ['Légumes', 'Fruits', 'Autres'],
            [rt.legumes, rt.fruits, rt.autres],
            [COLORS.yellow, COLORS.red, COLORS.cyan]
        );
        const total = rt.legumes + rt.fruits + rt.autres || 1;
        renderLegend('legend-repartition', [
            { color: COLORS.yellow, label: 'Légumes', value: Math.round(rt.legumes / total * 100) + '%' },
            { color: COLORS.red, label: 'Fruits', value: Math.round(rt.fruits / total * 100) + '%' },
            { color: COLORS.cyan, label: 'Autres', value: Math.round(rt.autres / total * 100) + '%' },
        ]);

        // Camembert surfaces par parcelle
        const surfaces = data.surfaces_parcelles || [];
        const surLabels = surfaces.map(s => s.nom);
        const surData = surfaces.map(s => s.surface);
        const surColors = surLabels.map((_, i) => PALETTE[i % PALETTE.length]);
        upsertDoughnut('chart-surfaces', surLabels, surData, surColors);
        renderLegend('legend-surfaces', surLabels.map((label, i) => ({
            color: surColors[i], label, value: surData[i], suffix: ' m²'
        })));

        // Camembert statuts
        const st = data.statuts;
        upsertDoughnut(
            'chart-statuts',
            ['En cours', 'À planifier', 'Récoltées'],
            [st.en_cours, st.a_planifier, st.recoltees],
            [COLORS.green, COLORS.yellow, COLORS.cyan]
        );
        const totalS = st.en_cours + st.a_planifier + st.recoltees || 1;
        renderLegend('legend-statuts', [
            { color: COLORS.green, label: 'En cours', value: Math.round(st.en_cours / totalS * 100) + '%' },
            { color: COLORS.yellow, label: 'À planifier', value: Math.round(st.a_planifier / totalS * 100) + '%' },
            { color: COLORS.cyan, label: 'Récoltées', value: Math.round(st.recoltees / totalS * 100) + '%' },
        ]);

        // Timeline
        renderTimeline(data.timeline);

        // Parcelles
        renderParcelles(data.parcelles);

        // Points
        const hp = data.historique_points || [];
        upsertLine('chart-points', hp.map(h => h.mois), hp.map(h => h.points));

        // Économie
        if (data.economie) {
            renderEconomie(data.economie, data);
        }

        // Historique valeur
        const hv = data.historique_valeur || [];
        if (hv.length > 0) {
            upsertLineValeur(
                'chart-historique-valeur',
                hv.map(h => h.mois),
                hv.map(h => h.potentielle),
                hv.map(h => h.realisee),
            );
        }
    }

    // ---- Chargement AJAX ----
    async function fetchStats(parcelle, periode) {
        const url = new URL(window.__URL_API_STATS__, window.location.origin);
        if (parcelle) url.searchParams.set('parcelle', parcelle);
        if (periode) url.searchParams.set('periode', periode);

        const resp = await fetch(url.toString(), {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (!resp.ok) throw new Error('Erreur serveur ' + resp.status);
        return resp.json();
    }

    async function appliquerFiltres() {
        const parcelle = document.getElementById('filter-parcelle').value;
        const periode = document.getElementById('filter-periode').value;
        const bar = document.getElementById('filters-bar');

        bar.classList.add('loading');

        try {
            const data = await fetchStats(parcelle, periode);
            renderAll(data);

            // Mise à jour de l'URL sans recharger (permet de partager le lien)
            const newUrl = new URL(window.location.href);
            if (parcelle) newUrl.searchParams.set('parcelle', parcelle);
            else newUrl.searchParams.delete('parcelle');
            if (periode) newUrl.searchParams.set('periode', periode);
            window.history.replaceState({}, '', newUrl.toString());
        } catch (err) {
            console.error('❌ Erreur stats:', err);
        } finally {
            bar.classList.remove('loading');
        }
    }

    // ---- Bootstrap ----
    document.addEventListener('DOMContentLoaded', function () {
        // Rendu initial avec les données du serveur (rapide)
        if (window.__STATS_INITIALES__) {
            renderAll(window.__STATS_INITIALES__);
        }

        // Écouteurs avec debounce
        const onChange = function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(appliquerFiltres, 300);
        };
        document.getElementById('filter-parcelle')?.addEventListener('change', onChange);
        document.getElementById('filter-periode')?.addEventListener('change', onChange);
    });

    // ============================================================
    // FORMATAGE MONÉTAIRE MULTI-DEVISE
    // ============================================================
    const DEVISES_CONFIG = {
        EUR: { symbole: '€', position: 'apres', decimales: 2 },
        USD: { symbole: '$', position: 'avant', decimales: 2 },
        GBP: { symbole: '£', position: 'avant', decimales: 2 },
        CHF: { symbole: 'CHF', position: 'apres', decimales: 2 },
        CAD: { symbole: 'C$', position: 'avant', decimales: 2 },
        XOF: { symbole: 'CFA', position: 'apres', decimales: 0 },
        XAF: { symbole: 'FCFA', position: 'apres', decimales: 0 },
        MAD: { symbole: 'DH', position: 'apres', decimales: 2 },
        DZD: { symbole: 'DA', position: 'apres', decimales: 2 },
        TND: { symbole: 'DT', position: 'apres', decimales: 2 },
        JPY: { symbole: '¥', position: 'avant', decimales: 0 },
        CNY: { symbole: '¥', position: 'avant', decimales: 2 },
        BRL: { symbole: 'R$', position: 'avant', decimales: 2 },
        MXN: { symbole: '$', position: 'avant', decimales: 2 },
        AUD: { symbole: 'A$', position: 'avant', decimales: 2 },
        INR: { symbole: '₹', position: 'avant', decimales: 2 },
        ZAR: { symbole: 'R', position: 'avant', decimales: 2 },
    };

    function formatMonnaie(montant, devise) {
        devise = devise || window.__DEVISE__ || 'EUR';
        const config = DEVISES_CONFIG[devise] || DEVISES_CONFIG.EUR;

        if (typeof montant !== 'number' || isNaN(montant)) return '0 ' + config.symbole;

        let montantStr;
        if (config.decimales === 0) {
            montantStr = Math.round(montant).toLocaleString('fr-FR');
        } else {
            montantStr = montant.toLocaleString('fr-FR', {
                minimumFractionDigits: config.decimales,
                maximumFractionDigits: config.decimales,
            });
        }

        return config.position === 'avant'
            ? `${config.symbole} ${montantStr}`
            : `${montantStr} ${config.symbole}`;
    }


    function getDeviseIcon(devise) {
        const icons = {
            EUR: '💶',
            USD: '💵',
            GBP: '💷',
            CHF: '🪙',
            CAD: '🍁',
            XOF: '🪙',
            XAF: '🪙',
            MAD: '🪙',
            DZD: '🪙',
            TND: '🪙',
            JPY: '💴',
            CNY: '🧧',
            BRL: '🪙',
            MXN: '🪙',
            AUD: '🪙',
            INR: '🪙',
            ZAR: '🪙',
        };
        return icons[devise] || '💰';
    }

    function renderEconomie(eco, data) {
        if (!eco) return;
        data = data || {}; // ✅ sécurisation

        // ============================================================
        // 1. VALEUR POTENTIELLE & RÉALISÉE
        // ============================================================
        const elPot = document.getElementById('valeur-potentielle');
        if (elPot) elPot.textContent = formatMonnaie(eco.valeur_potentielle, eco.devise);

        // ✅ NOUVEAU : badge devise
        const badge = document.getElementById('devise-badge');
        if (badge) badge.textContent = eco.devise || 'EUR';

        // ✅ NOUVEAU : icône devise dynamique
        const iconEl = document.getElementById('devise-icon');
        if (iconEl) {
            iconEl.textContent = getDeviseIcon(eco.devise);
        }

        const elRea = document.getElementById('valeur-realisee');
        if (elRea) elRea.textContent = formatMonnaie(eco.valeur_realisee, eco.devise);

        // ============================================================
        // 2. BARRE DE PROGRESSION
        // ============================================================
        const barre = document.getElementById('barre-realisee');
        if (barre) barre.style.width = (eco.pourcentage_realise || 0) + '%';

        const pct = document.getElementById('pct-realise');
        if (pct) pct.textContent = (eco.pourcentage_realise || 0) + '% réalisé';

        // ============================================================
        // 3. COMPARAISON MARCHÉ — annualisation intelligente
        // ============================================================
        const ecoAn = document.getElementById('economie-annuelle');
        if (ecoAn) {
            const histo = data.historique_valeur || [];
            const moisUniques = new Set(histo.map(h => h.mois));
            const nbMois = Math.max(1, moisUniques.size);
            const annuel = (eco.valeur_realisee / nbMois) * 12;
            ecoAn.textContent = formatMonnaie(annuel, eco.devise);

            const elDetail = document.getElementById('economie-detail');
            if (elDetail) {
                elDetail.textContent = `(sur ${nbMois} mois d'activité)`;
            }
        }

        // ============================================================
        // 4. TOP 3 CULTURES RENTABLES
        // ============================================================
        const el = document.getElementById('top-cultures-container');
        if (!el) return;

        if (!eco.top_cultures || eco.top_cultures.length === 0) {
            el.innerHTML = '<div style="color:#6c757d; text-align:center; padding:20px;">Ajoutez des cultures pour voir vos tops rentables.</div>';
            return;
        }

        const medals = ['🥇', '🥈', '🥉'];
        const borders = ['#ffd700', '#c0c0c0', '#cd7f32'];
        const bgs = ['rgba(255,215,0,0.12)', 'rgba(192,192,192,0.12)', 'rgba(205,127,50,0.12)'];

        el.innerHTML = eco.top_cultures.map((c, i) => `
            <div style="display: flex; align-items: center; gap: 12px; padding: 10px;
                        background: linear-gradient(90deg, ${bgs[i]}, transparent);
                        border-radius: 10px; border-left: 4px solid ${borders[i]};">
                <div style="font-size: 1.5rem;">${medals[i]}</div>
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        ${c.emoji || '🌱'} ${c.nom}
                    </div>
                    <div style="font-size: .75rem; color: #6c757d;">
                        ${c.nb_plants} plant(s) · ${formatMonnaie(c.valeur_contribuee_local, eco.devise)}
                    </div>
                </div>
                <div style="font-weight: 700; color: #28a745; white-space: nowrap;">
                    ${formatMonnaie(c.prix_local, eco.devise)}/kg
                </div>
            </div>
        `).join('');
    }

    function upsertLineValeur(id, labels, dataPot, dataRea) {
        const canvas = document.getElementById(id);
        if (!canvas) return;

        if (charts[id]) {
            charts[id].data.labels = labels;
            charts[id].data.datasets[0].data = dataPot;
            charts[id].data.datasets[1].data = dataRea;
            charts[id].update('none');
            return;
        }

        charts[id] = new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Potentiel',
                        data: dataPot,
                        borderColor: COLORS.green,
                        backgroundColor: 'rgba(40,167,69,.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 3,
                    },
                    {
                        label: 'Réalisé',
                        data: dataRea,
                        borderColor: COLORS.cyan,
                        backgroundColor: 'rgba(23,162,184,.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 3,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        backgroundColor: '#1b4332',
                        callbacks: {
                            label: (ctx) => ` ${ctx.dataset.label}: ${Math.round(ctx.parsed.y)} €`
                        }
                    }
                },
                scales: {
                    y: { beginAtZero: true, ticks: { callback: (v) => v + ' €' } },
                }
            }
        });
    }

})();