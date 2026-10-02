// Sentrillion — Endurion-inspired redesign concept
// Dependency-free interactions: preloader, staggered scroll reveal with
// SVG icon draw-in, count-up stats, cursor glow, magnetic tilt cards,
// sliding nav underline, hero parallax + split-text entrance, marquee
// ticker, mobile nav, announcement bar.

// Always control scroll position ourselves: never let a reload restore an
// old position or jump to a leftover #section in the address bar.
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

document.addEventListener('DOMContentLoaded', () => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const root = document.documentElement;

  // ---------- Footer year ----------
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---------- Preloader ----------
  const preloader = document.getElementById('preloader');
  const finishLoading = () => {
    if (preloader) preloader.classList.add('is-loaded');
    root.classList.add('hero-ready');
    setTimeout(() => { if (preloader) preloader.style.display = 'none'; }, 700);
  };
  if (reduceMotion) {
    finishLoading();
  } else {
    // Minimum display time so the preloader reads as intentional, not a flash.
    const minDelay = new Promise(res => setTimeout(res, 650));
    const pageLoad = new Promise(res => {
      if (document.readyState === 'complete') res();
      else window.addEventListener('load', res, { once: true });
    });
    Promise.all([minDelay, pageLoad]).then(finishLoading);
    // Safety net in case something never fires.
    setTimeout(finishLoading, 2500);
  }

  // ---------- Announcement bar ----------
  const announce = document.getElementById('announce');
  const announceClose = document.getElementById('announceClose');
  if (announceClose && announce) {
    announceClose.addEventListener('click', () => announce.classList.add('is-hidden'));
  }

  // ---------- Mobile menu toggle ----------
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('is-open');
      menuToggle.classList.toggle('is-active');
    });
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        menuToggle.classList.remove('is-active');
      });
    });
  }

  // ---------- Nav dropdown toggles (mobile) ----------
  document.querySelectorAll('.nav-caret').forEach(caret => {
    caret.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const item = caret.closest('.nav-item');
      if (!item) return;
      const isOpen = item.classList.toggle('is-open');
      caret.setAttribute('aria-expanded', String(isOpen));
    });
  });

  // ---------- Sliding nav underline ----------
  const navUnderline = document.getElementById('navUnderline');
  if (navUnderline && navLinks) {
    const links = navLinks.querySelectorAll('a');
    links.forEach(link => {
      link.addEventListener('mouseenter', () => {
        navUnderline.style.width = link.offsetWidth + 'px';
        navUnderline.style.transform = `translateX(${link.offsetLeft}px)`;
      });
    });
  }

  // ---------- Sticky nav shrink on scroll ----------
  const nav = document.getElementById('nav');
  if (nav) {
    const updateNav = () => {
      nav.classList.toggle('is-scrolled', window.scrollY > 30);
    };
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  }

  // ---------- Scroll reveal + SVG icon draw-in ----------
  const revealEls = document.querySelectorAll('.reveal');
  const prepIcons = (container) => {
    container.querySelectorAll('.draw-icon').forEach(icon => {
      if (typeof icon.getTotalLength !== 'function') return;
      const len = icon.getTotalLength();
      icon.style.strokeDasharray = len;
      icon.style.strokeDashoffset = len;
    });
  };
  const drawIcons = (container) => {
    container.querySelectorAll('.draw-icon').forEach(icon => {
      icon.style.strokeDashoffset = '0';
    });
  };
  document.querySelectorAll('.market-icon svg').forEach(prepIcons);

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          const icons = entry.target.querySelector('.market-icon svg');
          if (icons) requestAnimationFrame(() => drawIcons(entry.target));
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => observer.observe(el));
  } else {
    revealEls.forEach(el => {
      el.classList.add('is-visible');
      drawIcons(el);
    });
  }

  // ---------- Count-up stats ----------
  const statEls = document.querySelectorAll('.stat-num');
  if (statEls.length && 'IntersectionObserver' in window) {
    const easeOutExpo = (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t));
    const animateCount = (el) => {
      const target = parseFloat(el.dataset.count || '0');
      const suffix = el.dataset.suffix || '';
      const duration = 1400;
      const start = performance.now();
      const step = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const val = Math.round(target * easeOutExpo(progress));
        el.textContent = val + suffix;
        if (progress < 1) requestAnimationFrame(step);
      };
      if (reduceMotion) {
        el.textContent = target + suffix;
      } else {
        requestAnimationFrame(step);
      }
    };
    const statObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    statEls.forEach(el => statObserver.observe(el));
  }

  // ---------- Cursor glow (desktop, fine pointer only) ----------
  const cursorGlow = document.getElementById('cursorGlow');
  if (cursorGlow && !reduceMotion && window.matchMedia('(hover: hover)').matches) {
    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;
    let curX = targetX;
    let curY = targetY;
    let raf = null;

    const loop = () => {
      curX += (targetX - curX) * 0.12;
      curY += (targetY - curY) * 0.12;
      cursorGlow.style.transform = `translate3d(${curX}px, ${curY}px, 0)`;
      raf = requestAnimationFrame(loop);
    };

    window.addEventListener('mousemove', (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
      cursorGlow.classList.add('is-active');
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: true });

    document.addEventListener('mouseleave', () => cursorGlow.classList.remove('is-active'));
  }

  // ---------- Magnetic tilt on cards ----------
  if (!reduceMotion && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.tilt').forEach(card => {
      let rect = null;
      card.addEventListener('mouseenter', () => {
        rect = card.getBoundingClientRect();
      });
      card.addEventListener('mousemove', (e) => {
        if (!rect) rect = card.getBoundingClientRect();
        const px = (e.clientX - rect.left) / rect.width - 0.5;
        const py = (e.clientY - rect.top) / rect.height - 0.5;
        const rotX = (-py * 6).toFixed(2);
        const rotY = (px * 8).toFixed(2);
        card.style.transform = `perspective(700px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-2px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(700px) rotateX(0deg) rotateY(0deg) translateY(0)';
        rect = null;
      });
    });
  }

  // ---------- Hero background video ----------
  // Covers the homepage's flyover video (.hero-bg-img) as well as any
  // detail-page hero video (.page-hero-bg video), so reduced-motion and
  // autoplay-blocked handling stay consistent everywhere a video hero is used.
  document.querySelectorAll('.hero-bg-img, .page-hero-bg video').forEach((heroVideo) => {
    if (heroVideo.tagName !== 'VIDEO') return;
    if (reduceMotion) {
      // Respect reduced-motion: don't autoplay the footage, just show its
      // poster frame like a static photo.
      heroVideo.pause();
      heroVideo.removeAttribute('autoplay');
    } else {
      heroVideo.play().catch(() => {
        // Autoplay can be blocked by the browser; the poster image still
        // shows in that case, so there's nothing further to do.
      });
    }
  });

  // ---------- Hero targeting reticles ----------
  // A "computer-vision" scanning effect: small HUD reticles pop up at random
  // points along the hero footage, sweep from a neutral "scanning" state to
  // a red "confirmed" lock, then fade — like a sensor sweeping the terrain.
  const heroTargets = document.getElementById('heroTargets');
  if (heroTargets && !reduceMotion) {
    const MAX_ACTIVE = 2;
    let activeCount = 0;

    const codes = ['SCN', 'TGT', 'GRD', 'PTL', 'RCN'];
    const randomLabel = () => {
      const code = codes[Math.floor(Math.random() * codes.length)];
      const num = Math.floor(100 + Math.random() * 899);
      return `${code}-${num}`;
    };

    const spawnReticle = () => {
      if (activeCount >= MAX_ACTIVE || document.hidden) {
        scheduleNext();
        return;
      }
      activeCount++;

      const el = document.createElement('div');
      el.className = 'target-reticle';
      // Keep reticles low, over the terrain rather than the sky, and off the
      // right side away from the eyebrow/headline/sub-copy in the left column.
      const band = [58, 88];
      const x = 46 + Math.random() * 48;
      const y = band[0] + Math.random() * (band[1] - band[0]);
      el.style.left = x + '%';
      el.style.top = y + '%';
      el.innerHTML =
        '<svg viewBox="0 0 100 100" fill="none">' +
          '<g class="ring-outer"><circle cx="50" cy="50" r="46" stroke="currentColor" stroke-width="1" stroke-dasharray="4 7"/></g>' +
          '<circle cx="50" cy="50" r="32" stroke="currentColor" stroke-width="1" opacity="0.6"/>' +
          '<path d="M50 4V18M50 82V96M4 50H18M82 50H96" stroke="currentColor" stroke-width="1"/>' +
          '<path d="M14 14L24 24M86 14L76 24M14 86L24 76M86 86L76 76" stroke="currentColor" stroke-width="1.2"/>' +
          '<circle class="reticle-dot" cx="50" cy="50" r="2.4" fill="currentColor"/>' +
        '</svg>' +
        '<span class="target-label">' + randomLabel() + ' &middot; SCANNING</span>';
      heroTargets.appendChild(el);

      // Double rAF so the initial (pre-.is-active) state paints before the transition starts.
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-active')));

      const lockDelay = 900 + Math.random() * 500;
      const lockTimer = setTimeout(() => {
        el.classList.add('is-locked');
        const label = el.querySelector('.target-label');
        if (label) label.textContent = randomLabel() + ' · CONFIRMED';
      }, lockDelay);

      const holdTime = 2600 + Math.random() * 1400;
      const removeTimer = setTimeout(() => {
        el.classList.remove('is-active');
        setTimeout(() => {
          el.remove();
          activeCount--;
        }, 700);
      }, lockDelay + holdTime);

      // Guard against the tab going away mid-cycle leaving stray timers.
      el._cleanup = () => { clearTimeout(lockTimer); clearTimeout(removeTimer); };

      scheduleNext();
    };

    const scheduleNext = () => {
      const delay = 1800 + Math.random() * 2600;
      setTimeout(spawnReticle, delay);
    };

    // Two staggered chains so a couple of reticles can be visible at once.
    setTimeout(spawnReticle, 1300);
    setTimeout(spawnReticle, 3200);
  }

  // ---------- Hero parallax ----------
  const heroBg = document.getElementById('heroBg');
  const hero = document.getElementById('hero');
  if (heroBg && hero && !reduceMotion) {
    const updateParallax = () => {
      const rect = hero.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      const offset = rect.top * -0.12;
      heroBg.style.transform = `translate3d(0, ${offset}px, 0)`;
    };
    window.addEventListener('scroll', updateParallax, { passive: true });
    updateParallax();
  }

  // ---------- Scroll progress indicator ----------
  const indicator = document.getElementById('scrollIndicator');
  if (indicator) {
    const updateIndicator = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      indicator.style.height = pct + '%';
    };
    window.addEventListener('scroll', updateIndicator, { passive: true });
    updateIndicator();
  }

  // ---------- Plate-tracking laser dots ----------
  // Each dot rides a specific vehicle through the checkpoint video, driven
  // frame-by-frame from video.currentTime (not a CSS timer), so it can never
  // drift out of sync with the footage no matter how the clip loops or stalls.
  // Waypoints are [seconds, xPercent, yPercent] samples of that car's real
  // on-screen position (traced from the source footage), mapped here through
  // the video's object-fit:cover crop so the dot lands on-plate at any
  // viewport size.
  const plateLayer = document.querySelector('.plate-track-layer');
  if (plateLayer && !reduceMotion) {
    const heroBgEl = plateLayer.closest('.page-hero-bg');
    const plateVideo = heroBgEl ? heroBgEl.querySelector('video') : null;
    let tracks = {};
    try { tracks = JSON.parse(plateLayer.getAttribute('data-plate-tracks') || '{}'); } catch (e) { tracks = {}; }

    if (plateVideo && Object.keys(tracks).length) {
      const dots = {};
      Object.keys(tracks).forEach((key) => {
        const dot = document.createElement('div');
        dot.className = 'plate-dot';
        const core = document.createElement('div');
        core.className = 'plate-dot-core';
        dot.appendChild(core);
        plateLayer.appendChild(dot);
        dots[key] = dot;
      });

      const HOLD = 0.35; // seconds a dot stays visible just before/after its tracked window
      const interpolate = (waypoints, t) => {
        const first = waypoints[0];
        const last = waypoints[waypoints.length - 1];
        if (t <= first[0]) return (t >= first[0] - HOLD) ? first : null;
        if (t >= last[0]) return (t <= last[0] + HOLD) ? last : null;
        for (let i = 0; i < waypoints.length - 1; i++) {
          const a = waypoints[i], b = waypoints[i + 1];
          if (t >= a[0] && t <= b[0]) {
            const f = (b[0] === a[0]) ? 0 : (t - a[0]) / (b[0] - a[0]);
            return [t, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
          }
        }
        return null;
      };

      const tick = () => {
        const vw = plateVideo.videoWidth;
        const vh = plateVideo.videoHeight;
        if (!vw || !vh) { requestAnimationFrame(tick); return; }
        const rect = plateLayer.getBoundingClientRect();
        if (rect.width && rect.height) {
          const videoAspect = vw / vh;
          const boxAspect = rect.width / rect.height;
          let scale, offsetX = 0, offsetY = 0;
          if (boxAspect > videoAspect) {
            scale = rect.width / vw;
            offsetY = (vh * scale - rect.height) / 2;
          } else {
            scale = rect.height / vh;
            offsetX = (vw * scale - rect.width) / 2;
          }
          const t = plateVideo.currentTime;
          Object.keys(tracks).forEach((key) => {
            const wp = interpolate(tracks[key], t);
            const dot = dots[key];
            if (!wp) { dot.classList.remove('is-active'); return; }
            const px = (wp[1] / 100) * vw * scale - offsetX;
            const py = (wp[2] / 100) * vh * scale - offsetY;
            // Set directly on .transform (not a custom property read inside
            // a running @keyframes) so nothing else is interpolating this
            // element's transform and the dot snaps exactly to (px, py)
            // every frame with no lag or drift.
            dot.style.transform = 'translate(' + px.toFixed(1) + 'px, ' + py.toFixed(1) + 'px)';
            dot.classList.add('is-active');
          });
        }
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }
  // ---------- Operational Memory: parallax, timecode, network console ----------
  const omBg = document.getElementById('omNumbersBg');
  if (omBg && !reduceMotion) {
    const omSec = omBg.parentElement;
    window.addEventListener('scroll', () => {
      const r = omSec.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      omBg.style.transform = 'scale(1.08) translateY(' + (p * 40).toFixed(1) + 'px)';
    }, { passive: true });
  }

  const omTc = document.getElementById('omTimecode');
  if (omTc) {
    const tc0 = performance.now();
    const pad2 = (n) => String(n).padStart(2, '0');
    setInterval(() => {
      const s = (performance.now() - tc0) / 1000;
      omTc.textContent = '00:' + pad2(Math.floor(s / 60)) + ':' + pad2(Math.floor(s % 60)) + ':' + pad2(Math.floor((s % 1) * 30));
    }, 1000 / 15);
  }

  const omCv = document.getElementById('omNetmap');
  if (omCv && omCv.getContext) {
    const ctx = omCv.getContext('2d');
    let W = 0, H = 0;
    const resize = () => {
      const r = omCv.getBoundingClientRect();
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      W = r.width; H = r.height;
      omCv.width = W * dpr; omCv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    window.addEventListener('resize', resize);

    // Seeded random so the illustrative site layout is identical on every load.
    let seed = 11;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const border = [];
    for (let i = 0; i <= 40; i++) {
      const x = i / 40;
      const y = 0.30 + 0.07 * Math.sin(x * 5.2) + 0.04 * Math.sin(x * 13.1 + 1.3) + (x > 0.55 ? (x - 0.55) * 0.35 : 0);
      border.push([x, y]);
    }
    const sites = [];
    const REGIONS = ['SDC', 'ELC', 'TCA', 'EPT', 'BBT', 'DRT', 'LRT', 'RGV'];
    const TYPES = ['PTZ', 'FIX', 'LPR', 'THM'];
    for (let i = 1; i < 40; i++) {
      if (rnd() < 0.35) continue;
      const [x, y] = border[i];
      sites.push({ x: x + (rnd() - 0.5) * 0.01, y: y + 0.02 + rnd() * 0.05, state: 0, t: 0 });
      if (rnd() < 0.5) sites.push({ x: x + (rnd() - 0.5) * 0.02, y: y + 0.12 + rnd() * 0.32, state: 0, t: 0 });
    }
    sites.forEach((s, i) => {
      s.id = REGIONS[Math.min(REGIONS.length - 1, Math.floor(s.x * REGIONS.length))] + '-' + String(100 + (i * 7) % 900).padStart(3, '0');
      s.type = TYPES[i % TYPES.length];
      s.hist = 2 + Math.floor(rnd() * 14);
    });
    const ops = { x: 0.52, y: 0.84 };
    const elOnline = document.getElementById('omOnline');
    const elOpen = document.getElementById('omOpen');
    const elRest = document.getElementById('omRestored');
    const log = document.getElementById('omLog');
    const FAULTS = ['Video loss', 'PTZ drift', 'Link down', 'Power fault', 'Encoder fault', 'Lens fogging'];
    let restored = 38;
    let wo = 48213;
    const clock = () => {
      const d = new Date();
      const p = (n) => String(n).padStart(2, '0');
      return p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
    };
    const addLog = (html) => {
      const line = document.createElement('div');
      line.className = 'om-log-line';
      line.innerHTML = '<span class="t">' + clock() + '</span>' + html;
      log.prepend(line);
      while (log.children.length > 9) log.lastChild.remove();
    };
    const trigger = () => {
      const idle = sites.filter((s) => s.state === 0);
      if (!idle.length) return;
      const s = idle[Math.floor(Math.random() * idle.length)];
      s.state = 1; s.t = performance.now(); s.wo = ++wo; s.hist += 1;
      s.fault = FAULTS[Math.floor(Math.random() * FAULTS.length)];
      addLog('<span class="fail">FAULT</span>&nbsp; ' + s.id + ' ' + s.type + ' &middot; ' + s.fault + ' &middot; WO-' + s.wo + ' &middot; ' + s.hist + ' prior');
      setTimeout(() => {
        s.state = 2; s.t = performance.now(); restored++;
        addLog('<span class="ok">RESTORED</span> ' + s.id + ' &middot; WO-' + s.wo + ' closed &middot; ' + (18 + Math.floor(Math.random() * 70)) + 'm');
        setTimeout(() => { s.state = 0; }, 2400);
      }, 2600 + Math.random() * 3200);
    };
    for (let i = 0; i < 4; i++) {
      addLog('<span class="ok">RESTORED</span> ' + sites[(i * 5) % sites.length].id + ' &middot; WO-' + (48200 + i * 3) + ' closed &middot; ' + (22 + i * 9) + 'm');
    }

    // Only animate while the console is on screen.
    let omVisible = false;
    let omTimer = null;
    const draw = (now) => {
      ctx.clearRect(0, 0, W, H);
      ctx.strokeStyle = 'rgba(255,255,255,0.045)';
      ctx.lineWidth = 1;
      for (let gx = 0; gx <= W; gx += W / 16) { ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke(); }
      for (let gy = 0; gy <= H; gy += H / 8) { ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke(); }
      ctx.setLineDash([4, 5]);
      ctx.strokeStyle = 'rgba(245,245,244,0.35)';
      ctx.beginPath();
      border.forEach(([x, y], i) => (i ? ctx.lineTo(x * W, y * H) : ctx.moveTo(x * W, y * H)));
      ctx.stroke();
      ctx.setLineDash([]);
      const ox = ops.x * W, oy = ops.y * H;
      ctx.strokeStyle = 'rgba(245,245,244,0.6)';
      ctx.strokeRect(ox - 5, oy - 5, 10, 10);
      ctx.fillStyle = 'rgba(154,154,157,0.9)';
      ctx.font = '9px "JetBrains Mono", monospace';
      ctx.fillText('OPS CENTER', ox + 10, oy + 3);
      let open = 0;
      sites.forEach((s) => {
        const x = s.x * W, y = s.y * H;
        if (s.state === 1) {
          open++;
          const age = (now - s.t) / 1000;
          const k = Math.min(1, age / 0.8);
          ctx.strokeStyle = 'rgba(232,40,63,0.45)';
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (ox - x) * k, y + (oy - y) * k); ctx.stroke();
          const rr = 4 + ((age * 18) % 18);
          ctx.strokeStyle = 'rgba(232,40,63,' + (1 - rr / 22).toFixed(2) + ')';
          ctx.beginPath(); ctx.arc(x, y, rr, 0, Math.PI * 2); ctx.stroke();
          ctx.fillStyle = '#e8283f';
          ctx.beginPath(); ctx.arc(x, y, 3.2, 0, Math.PI * 2); ctx.fill();
          ctx.fillText(s.id, x + 7, y - 6);
        } else if (s.state === 2) {
          const a = Math.max(0, 1 - (now - s.t) / 2400);
          ctx.fillStyle = 'rgba(127,209,168,' + (0.35 + 0.65 * a).toFixed(2) + ')';
          ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill();
          ctx.strokeStyle = 'rgba(127,209,168,' + (0.6 * a).toFixed(2) + ')';
          ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI * 2); ctx.stroke();
        } else {
          ctx.fillStyle = 'rgba(245,245,244,0.75)';
          ctx.beginPath(); ctx.arc(x, y, 1.8, 0, Math.PI * 2); ctx.fill();
        }
      });
      elOnline.textContent = sites.length - open;
      elOpen.textContent = open;
      elRest.textContent = restored;
      if (omVisible && !reduceMotion) requestAnimationFrame(draw);
    };
    if (reduceMotion) {
      trigger(); trigger();
      setTimeout(() => draw(performance.now()), 50);
    } else if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          const was = omVisible;
          omVisible = e.isIntersecting;
          if (omVisible && !was) {
            if (e.target.getBoundingClientRect().width) resize();
            requestAnimationFrame(draw);
            omTimer = setInterval(trigger, 1500);
          } else if (!omVisible && omTimer) {
            clearInterval(omTimer); omTimer = null;
          }
        });
      }).observe(omCv);
    }
  }
  // ---------- Hero terrain flight ----------
  // A slow flight over procedurally generated terrain following the border
  // (red dashed line), with port-of-entry masts that fault and restore.
  // Illustrative only: no real port names or locations.
  const terrainCv = document.getElementById('heroTerrain');
  if (terrainCv && terrainCv.getContext) {
    const tctx = terrainCv.getContext('2d');
    const coordEl = document.getElementById('heroCoord');
    const hdgEl = document.getElementById('heroHdg');
    const statusEl = document.getElementById('heroStatus');
    let TW = 0, TH = 0, COLS = 150, ROWS = 95;
    const tResize = () => {
      const r = terrainCv.getBoundingClientRect();
      // Thin lines don't need full retina resolution; capping the backing
      // store keeps each frame cheap on high-DPI laptops.
      const dpr = Math.min(1.5, window.devicePixelRatio || 1);
      TW = r.width; TH = r.height;
      terrainCv.width = Math.round(TW * dpr); terrainCv.height = Math.round(TH * dpr);
      tctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const small = TW < 700;
      COLS = Math.max(40, Math.round(TW / (small ? 8 : 10)));
      ROWS = small ? 55 : 80;
    };
    tResize();
    window.addEventListener('resize', tResize);

    const hash = (x, z) => {
      let h = x * 374761393 + z * 668265263;
      h = (h ^ (h >>> 13)) * 1274126177;
      return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
    };
    const noise = (x, z) => {
      const xi = Math.floor(x), zi = Math.floor(z);
      const xf = x - xi, zf = z - zi;
      const u = xf * xf * (3 - 2 * xf), v = zf * zf * (3 - 2 * zf);
      const a = hash(xi, zi), b = hash(xi + 1, zi), c = hash(xi, zi + 1), d = hash(xi + 1, zi + 1);
      return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
    };
    const borderX = (z) => Math.sin(z * 0.0042) * 90 + Math.sin(z * 0.011 + 1.7) * 30;
    const height = (x, z) => {
      let h = 0, amp = 1, f = 0.0045;
      for (let o = 0; o < 3; o++) { h += amp * noise(x * f, z * f); amp *= 0.42; f *= 2.3; }
      const valley = Math.min(1, Math.abs(x - borderX(z)) / 160);
      return (h - 0.75) * 150 * (0.18 + 0.82 * valley);
    };
    const SPACING = 340;
    const portState = (k, t) => {
      const r = hash(k, 7);
      if (r > 0.33) return 0;
      const cycle = 9 + r * 20;
      const ph = ((t / 1000 + r * 50) % cycle) / cycle;
      if (ph < 0.22) return 1;
      if (ph < 0.34) return 2;
      return 0;
    };

    let running = false;
    let tStart = performance.now();
    const drawTerrain = (now) => {
      const t = now - tStart;
      const camZ = reduceMotion ? 0 : t * 0.055;
      const camX = borderX(camZ + 260) * 0.85 + 70;
      const camY = 150 + Math.sin(t * 0.00025) * 12;
      const yaw = Math.atan2(borderX(camZ + 700) - borderX(camZ + 200), 500) * 0.6;
      const cy = Math.cos(yaw), sy = Math.sin(yaw);
      const f = Math.max(TW, TH) * 0.9;
      const small = TW < 700;
      const horizon = TH * (small ? 0.6 : 0.4);
      const cx = TW * (small ? 0.5 : 0.62);
      const project = (x, y, z) => {
        const dx = x - camX, dz = z - camZ;
        const rx = dx * cy - dz * sy, rz = dx * sy + dz * cy;
        if (rz < 8) return null;
        return [cx + rx * f / rz, horizon + (camY - y) * f / rz, rz];
      };

      tctx.clearRect(0, 0, TW, TH);
      const NEAR = 30, FAR = 2600;
      const DZ = (FAR - NEAR) / ROWS;
      const zBase = Math.floor(camZ / DZ) * DZ;

      // Floating-horizon hidden-line removal: draw rows near to far, sampling
      // fixed screen columns, and only draw where a row rises above
      // everything already drawn in front of it. No per-row fills, so the
      // cost is a few thousand points and ~80 strokes per frame.
      const ymin = new Float32Array(COLS + 1).fill(TH + 50);
      for (let i = 0; i <= ROWS; i++) {
        const z = zBase + NEAR + i * DZ;
        const dz = z - camZ;
        if (dz < NEAR * 0.5) continue;
        const rel = dz / FAR;
        const alpha = 0.07 + Math.pow(Math.max(0, 1 - rel), 1.5) * 0.6;
        tctx.beginPath();
        let prevVisible = false;
        for (let j = 0; j <= COLS; j++) {
          const sxp = (j / COLS) * TW;
          const k = (sxp - cx) / f;
          const den = cy - k * sy;
          if (Math.abs(den) < 1e-4) { prevVisible = false; continue; }
          const dx = dz * (sy + k * cy) / den;
          const x = camX + dx;
          const rz = dx * sy + dz * cy;
          if (rz < 8) { prevVisible = false; continue; }
          const syp = horizon + (camY - height(x, z)) * f / rz;
          if (syp < ymin[j]) {
            if (prevVisible) tctx.lineTo(sxp, syp); else tctx.moveTo(sxp, syp);
            ymin[j] = syp;
            prevVisible = true;
          } else {
            prevVisible = false;
          }
        }
        tctx.strokeStyle = 'rgba(245,245,244,' + alpha.toFixed(3) + ')';
        tctx.lineWidth = 1;
        tctx.stroke();
      }

      // The border line: a soft wide stroke under a crisp dashed one
      // (cheaper than shadowBlur).
      tctx.beginPath();
      let s = false;
      for (let z = camZ + NEAR; z < camZ + FAR; z += 14) {
        const x = borderX(z);
        const p = project(x, height(x, z) + 2, z);
        if (!p) { s = false; continue; }
        if (!s) { tctx.moveTo(p[0], p[1]); s = true; } else tctx.lineTo(p[0], p[1]);
      }
      tctx.strokeStyle = 'rgba(232,40,63,0.16)';
      tctx.lineWidth = 5;
      tctx.stroke();
      const grad = tctx.createLinearGradient(0, horizon, 0, TH);
      grad.addColorStop(0, 'rgba(232,40,63,0.35)');
      grad.addColorStop(1, 'rgba(232,40,63,1)');
      tctx.setLineDash([10, 6]);
      tctx.strokeStyle = grad;
      tctx.lineWidth = 1.6;
      tctx.stroke();
      tctx.setLineDash([]);

      // Ports of entry
      let faults = 0;
      const k0 = Math.ceil((camZ + NEAR) / SPACING);
      for (let k = k0; k * SPACING < camZ + FAR; k++) {
        const z = k * SPACING + (hash(k, 3) - 0.5) * 80;
        const x = borderX(z);
        const y = height(x, z);
        const base = project(x, y, z);
        const top = project(x, y + 60, z);
        if (!base || !top) continue;
        const a = Math.max(0, 1 - ((z - camZ) / FAR) * 1.1);
        const st = portState(k, t);
        const col = st === 1 ? '232,40,63' : st === 2 ? '127,209,168' : '245,245,244';
        if (st === 1 && a > 0.25) faults++;
        tctx.strokeStyle = 'rgba(' + col + ',' + (0.55 * a).toFixed(2) + ')';
        tctx.lineWidth = 1;
        tctx.beginPath(); tctx.moveTo(base[0], base[1]); tctx.lineTo(top[0], top[1]); tctx.stroke();
        const rad = Math.max(1.5, 900 / base[2]);
        const g = tctx.createRadialGradient(top[0], top[1], 0, top[0], top[1], rad * 5);
        g.addColorStop(0, 'rgba(' + col + ',' + (0.55 * a).toFixed(2) + ')');
        g.addColorStop(1, 'rgba(' + col + ',0)');
        tctx.fillStyle = g;
        tctx.beginPath(); tctx.arc(top[0], top[1], rad * 5, 0, Math.PI * 2); tctx.fill();
        tctx.fillStyle = 'rgba(' + col + ',' + a.toFixed(2) + ')';
        tctx.beginPath(); tctx.arc(top[0], top[1], rad, 0, Math.PI * 2); tctx.fill();
        if (st === 1) {
          const ph = (t / 90) % 6;
          tctx.strokeStyle = 'rgba(232,40,63,' + (0.8 * a * (1 - ph / 6)).toFixed(2) + ')';
          tctx.beginPath(); tctx.arc(top[0], top[1], rad * (2 + ph), 0, Math.PI * 2); tctx.stroke();
        }
        tctx.strokeStyle = 'rgba(' + col + ',' + (0.25 * a).toFixed(2) + ')';
        tctx.beginPath(); tctx.ellipse(base[0], base[1], rad * 4, rad * 1.3, 0, 0, Math.PI * 2); tctx.stroke();
        if (!small && base[2] < 1100 && a > 0.3) {
          tctx.font = '10px "JetBrains Mono", monospace';
          tctx.fillStyle = 'rgba(' + col + ',' + (0.85 * a).toFixed(2) + ')';
          tctx.fillText('POE ' + String(k % 100).padStart(2, '0') + (st === 1 ? ' · FAULT' : st === 2 ? ' · RESTORED' : ' · NOMINAL'), top[0] + rad + 8, top[1] + 3);
        }
      }

      if (coordEl) coordEl.textContent = (31.334 + Math.sin(camZ * 0.0003) * 0.02).toFixed(4) + ' N  ' + (110.943 - camZ * 0.00002).toFixed(4) + ' W';
      if (hdgEl) hdgEl.textContent = String(Math.round((92 + yaw * 57.3 + 360) % 360)).padStart(3, '0');
      if (statusEl) statusEl.textContent = faults ? faults + (faults > 1 ? ' ports' : ' port') + ' in fault · dispatch active' : 'All ports nominal';

      if (running && !reduceMotion) requestAnimationFrame(drawTerrain);
    };

    if (reduceMotion) {
      requestAnimationFrame(drawTerrain);
    } else if ('IntersectionObserver' in window) {
      // Only burn frames while the hero is on screen.
      new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          const was = running;
          running = e.isIntersecting;
          if (running && !was) requestAnimationFrame(drawTerrain);
        });
      }).observe(terrainCv);
    } else {
      running = true;
      requestAnimationFrame(drawTerrain);
    }
  }
  // ---------- Logo returns to the very top ----------
  // On the homepage, scroll all the way up (above the announcement bar)
  // instead of reloading; inner pages link to index.html, which loads at top.
  const logoHome = document.getElementById('logoHome');
  if (logoHome) {
    logoHome.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      if (location.hash) history.replaceState(null, '', location.pathname + location.search);
    });
  }
  // ---------- Section links without sticky hashes ----------
  // In-page links (#contact, #memory, ...) scroll smoothly but never leave a
  // hash in the address bar, so a later reload opens at the top instead of
  // jumping to that section. Arriving from another page via
  // index.html#section still lands on the section, then the hash is cleared.
  const stripHash = () => {
    if (location.hash) history.replaceState(null, '', location.pathname + location.search);
  };
  const scrollToId = (id, smooth) => {
    const target = id && document.getElementById(id);
    if (!target) return false;
    target.scrollIntoView({ behavior: smooth && !reduceMotion ? 'smooth' : 'auto', block: 'start' });
    return true;
  };
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    if (!id) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }); return; }
    if (scrollToId(id, true)) { e.preventDefault(); stripHash(); }
  });
  window.addEventListener('hashchange', () => {
    if (scrollToId(location.hash.slice(1), true)) stripHash();
  });
  const navEntry = performance.getEntriesByType ? performance.getEntriesByType('navigation')[0] : null;
  const cameByLink = !navEntry || navEntry.type === 'navigate';
  const arrivalId = location.hash.slice(1);
  if (arrivalId && cameByLink && document.getElementById(arrivalId)) {
    // Wait a frame so layout (fonts, hero height) settles before jumping.
    requestAnimationFrame(() => { scrollToId(arrivalId, false); stripHash(); });
  } else {
    stripHash();
    // Hold the page at the top for the first couple of seconds after load,
    // in case the hosting frame (or the browser) tries to restore an old
    // scroll position. Any real input from the visitor ends the hold
    // immediately, so it never fights someone who starts scrolling.
    window.scrollTo({ top: 0, behavior: 'instant' });
    let holding = true;
    const release = () => {
      holding = false;
      ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach((ev) => window.removeEventListener(ev, release, true));
    };
    ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach((ev) => window.addEventListener(ev, release, { capture: true, passive: true }));
    const pin = () => { if (holding && window.scrollY !== 0) window.scrollTo({ top: 0, behavior: 'instant' }); };
    window.addEventListener('scroll', pin, { passive: true });
    window.addEventListener('load', pin);
    setTimeout(() => { release(); window.removeEventListener('scroll', pin); }, 2500);
  }
  // ---------- In the field: rain over the bucket-truck footage ----------
  const rainCv = document.getElementById('omRain');
  if (rainCv && rainCv.getContext && !reduceMotion) {
    const rctx = rainCv.getContext('2d');
    let RW = 0, RH = 0, drops = [], rainOn = false;
    const rainResize = () => {
      const r = rainCv.getBoundingClientRect();
      const dpr = Math.min(1.5, window.devicePixelRatio || 1);
      RW = r.width; RH = r.height;
      rainCv.width = Math.round(RW * dpr); rainCv.height = Math.round(RH * dpr);
      rctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round((RW * RH) / 5200);
      drops = Array.from({ length: n }, () => {
        const z = Math.random();              // depth: 0 far, 1 near
        return { x: Math.random() * RW, y: Math.random() * RH, z,
                 len: 10 + z * 26, v: 9 + z * 16, a: 0.08 + z * 0.22 };
      });
    };
    rainResize();
    window.addEventListener('resize', rainResize);
    const WIND = 0.18;
    const drawRain = () => {
      rctx.clearRect(0, 0, RW, RH);
      rctx.lineCap = 'round';
      for (const d of drops) {
        rctx.strokeStyle = 'rgba(220,226,232,' + d.a.toFixed(3) + ')';
        rctx.lineWidth = 0.6 + d.z * 0.9;
        rctx.beginPath();
        rctx.moveTo(d.x, d.y);
        rctx.lineTo(d.x - d.len * WIND, d.y + d.len);
        rctx.stroke();
        d.y += d.v; d.x -= d.v * WIND;
        if (d.y > RH || d.x < -40) { d.y = -d.len - Math.random() * 80; d.x = Math.random() * (RW + 80); }
      }
      if (rainOn) requestAnimationFrame(drawRain);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          const was = rainOn;
          rainOn = e.isIntersecting;
          if (rainOn && !was) { rainResize(); requestAnimationFrame(drawRain); }
        });
      }).observe(rainCv);
    }
  }
});
