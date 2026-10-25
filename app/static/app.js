(() => {
  'use strict';

  const MAX_FILE_BYTES = 20 * 1024 * 1024;
  const MAX_DURATION_SECONDS = 10 * 60;
  const fileInput = document.getElementById('audio-file');
  const dropzone = document.getElementById('dropzone');
  const audioPreview = document.getElementById('audio-preview');
  const selectedFile = document.getElementById('selected-file');
  const fileName = document.getElementById('file-name');
  const fileSize = document.getElementById('file-size');
  const fileReady = document.getElementById('file-ready');
  const affirmationCheck = document.getElementById('affirmation');
  const analyzeBtn = document.getElementById('analyze-btn');
  const analyzeButtonLabel = document.getElementById('analyze-button-label');
  const analyzeHelp = document.getElementById('analyze-help');
  const clearBtn = document.getElementById('clear-btn');
  const progressPanel = document.getElementById('analysis-progress');
  const progressLabel = document.getElementById('progress-label');
  const progressState = document.getElementById('progress-state');
  const resultsContainer = document.getElementById('results-container');
  const resultsSummary = document.getElementById('results-summary');
  const voiceInterpretation = document.getElementById('voice-interpretation');
  const windowLabelList = document.getElementById('window-label-list');
  const radarCard = document.getElementById('radar-card');
  const radarChart = document.getElementById('radar-chart');
  const radarWindowSelect = document.getElementById('radar-window-select');
  const radarWindowLegend = document.getElementById('radar-window-legend');
  const radarWindowLabel = document.getElementById('radar-window-label');
  const summarySegments = document.getElementById('summary-segments');
  const summaryDuration = document.getElementById('summary-duration');
  const summaryDevice = document.getElementById('summary-device');

  let currentObjectUrl = null;
  let activeSegmentEnd = null;
  let selectedFileIsValid = false;
  let fileValidationMessage = '';
  let isAnalyzing = false;
  let activeSegments = [];

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatBytes(bytes) {
    if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  function formatDuration(seconds) {
    const total = Math.max(0, Math.round(Number(seconds) || 0));
    const minutes = Math.floor(total / 60);
    const remainder = total % 60;
    return `${minutes}:${String(remainder).padStart(2, '0')}`;
  }

  function showEmptyState(title, copy) {
    resultsContainer.className = 'empty-state';
    resultsContainer.setAttribute('aria-busy', 'false');
    resultsContainer.innerHTML = `
      <div class="empty-inner">
        <span class="empty-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5m0 14h16M8 15v-4m4 4V7m4 8v-6"/></svg>
        </span>
        <p class="empty-title">${escapeHtml(title)}</p>
        <p class="empty-copy">${escapeHtml(copy)}</p>
      </div>`;
  }

  function updateControls() {
    const hasFile = Boolean(fileInput.files && fileInput.files.length);
    const ready = hasFile && selectedFileIsValid && affirmationCheck.checked;
    analyzeBtn.disabled = !ready || isAnalyzing;
    clearBtn.disabled = isAnalyzing;
    analyzeButtonLabel.textContent = isAnalyzing ? 'Analyzing…' : 'Analyze recording';

    if (isAnalyzing) {
      analyzeHelp.textContent = 'Analysis is running on the local CallSense server.';
      analyzeHelp.className = 'helper-status';
    } else if (!hasFile) {
      analyzeHelp.textContent = 'Choose a WAV or MP3 file to begin.';
      analyzeHelp.className = 'helper-status';
    } else if (!selectedFileIsValid) {
      analyzeHelp.textContent = fileValidationMessage || 'Choose a supported audio file.';
      analyzeHelp.className = 'helper-status is-error';
    } else if (!affirmationCheck.checked) {
      analyzeHelp.textContent = 'Check the authorization box above to enable analysis.';
      analyzeHelp.className = 'helper-status';
    } else {
      analyzeHelp.textContent = 'Ready. Select Analyze recording to continue.';
      analyzeHelp.className = 'helper-status is-ready';
    }
  }

  function resetResults() {
    resultsSummary.classList.remove('is-visible');
    resultsSummary.setAttribute('aria-hidden', 'true');
    voiceInterpretation.classList.remove('is-visible');
    voiceInterpretation.setAttribute('aria-hidden', 'true');
    windowLabelList.replaceChildren();
    radarCard.classList.remove('is-visible');
    radarCard.setAttribute('aria-hidden', 'true');
    radarWindowLegend.style.display = 'none';
    radarWindowSelect.replaceChildren(new Option('Recording average', ''));
    activeSegments = [];
    showEmptyState('Your timeline will appear here', 'Choose a recording and confirm authorization to start a local analysis.');
  }

  const preferredEmotionOrder = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'other', 'sad', 'surprised', 'unknown'];
  const chartFrame = { width: 560, height: 430, cx: 280, cy: 211, radius: 142, labelRadius: 173 };
  const springRuns = new WeakMap();
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function runSpring(element, key, from, to, { stiffness, damping, mass = 1, delay = 0 }, update) {
    let runs = springRuns.get(element);
    if (!runs) {
      runs = new Map();
      springRuns.set(element, runs);
    }
    runs.get(key)?.cancel();

    if (reducedMotion.matches) {
      update(to);
      return;
    }

    const run = { cancelled: false, frame: 0 };
    runs.set(key, run);
    const startAt = performance.now() + delay * 1000;
    const naturalFrequency = Math.sqrt(stiffness / mass);
    const dampingRatio = damping / (2 * Math.sqrt(stiffness * mass));
    const displacement = from - to;
    let valueAt = (time) => to;
    let velocityAt = (time) => 0;

    if (dampingRatio < 1) {
      const dampedFrequency = naturalFrequency * Math.sqrt(1 - dampingRatio ** 2);
      const sineCoefficient = (dampingRatio * naturalFrequency * displacement) / dampedFrequency;
      valueAt = (time) => {
        const envelope = Math.exp(-dampingRatio * naturalFrequency * time);
        return to + envelope * (displacement * Math.cos(dampedFrequency * time) + sineCoefficient * Math.sin(dampedFrequency * time));
      };
      velocityAt = (time) => {
        const envelope = Math.exp(-dampingRatio * naturalFrequency * time);
        const cosineTerm = -displacement * dampedFrequency * Math.sin(dampedFrequency * time);
        const sineTerm = sineCoefficient * dampedFrequency * Math.cos(dampedFrequency * time);
        return envelope * (cosineTerm + sineTerm - dampingRatio * naturalFrequency * (displacement * Math.cos(dampedFrequency * time) + sineCoefficient * Math.sin(dampedFrequency * time)));
      };
    } else if (Math.abs(dampingRatio - 1) < 0.0001) {
      valueAt = (time) => to + Math.exp(-naturalFrequency * time) * displacement * (1 + naturalFrequency * time);
      velocityAt = (time) => -Math.exp(-naturalFrequency * time) * displacement * naturalFrequency ** 2 * time;
    } else {
      const root = Math.sqrt(dampingRatio ** 2 - 1);
      const firstRoot = -naturalFrequency * (dampingRatio - root);
      const secondRoot = -naturalFrequency * (dampingRatio + root);
      const firstCoefficient = (-secondRoot * displacement) / (firstRoot - secondRoot);
      const secondCoefficient = displacement - firstCoefficient;
      valueAt = (time) => to + firstCoefficient * Math.exp(firstRoot * time) + secondCoefficient * Math.exp(secondRoot * time);
      velocityAt = (time) => firstRoot * firstCoefficient * Math.exp(firstRoot * time) + secondRoot * secondCoefficient * Math.exp(secondRoot * time);
    }

    run.cancel = () => {
      run.cancelled = true;
      if (run.frame) cancelAnimationFrame(run.frame);
    };

    function tick(now) {
      if (run.cancelled) return;
      if (now < startAt) {
        run.frame = requestAnimationFrame(tick);
        return;
      }
      const elapsed = (now - startAt) / 1000;
      const value = valueAt(elapsed);
      const velocity = velocityAt(elapsed);
      update(value);

      if (Math.abs(to - value) < 0.01 && Math.abs(velocity) < 0.01) {
        update(to);
        if (runs.get(key) === run) runs.delete(key);
        return;
      }
      run.frame = requestAnimationFrame(tick);
    }

    run.frame = requestAnimationFrame(tick);
  }

  function bezierYForX(x, points) {
    const [x1, y1, x2, y2] = points;
    const coordinate = (t, p1, p2) => 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3;
    let low = 0;
    let high = 1;
    for (let i = 0; i < 16; i += 1) {
      const middle = (low + high) / 2;
      if (coordinate(middle, x1, x2) < x) low = middle;
      else high = middle;
    }
    return coordinate((low + high) / 2, y1, y2);
  }

  function runTween(durationMs, delayMs, update) {
    if (reducedMotion.matches) {
      update(1);
      return;
    }
    const start = performance.now() + delayMs;
    const ease = [0.85, 0, 0.15, 1];
    function tick(now) {
      const linear = Math.max(0, Math.min(1, (now - start) / durationMs));
      update(bezierYForX(linear, ease));
      if (linear < 1) requestAnimationFrame(tick);
      else update(1);
    }
    requestAnimationFrame(tick);
  }

  function scoreValue(segment, key) {
    const raw = Number(segment?.scores?.[key]);
    return Number.isFinite(raw) ? Math.max(0, Math.min(1, raw)) : 0;
  }

  function radarPoint(index, count, value, radius = chartFrame.radius) {
    const angle = -Math.PI / 2 + (Math.PI * 2 * index) / count;
    const distance = radius * (Math.max(0, Math.min(100, value)) / 100);
    return {
      x: chartFrame.cx + Math.cos(angle) * distance,
      y: chartFrame.cy + Math.sin(angle) * distance,
      angle
    };
  }

  function gridPolygonPoints(count, scale = 1) {
    return Array.from({ length: count }, (_, index) => {
      const angle = -Math.PI / 2 + (2 * Math.PI * (index + 0.5)) / count;
      const distance = chartFrame.radius * scale;
      const point = { x: chartFrame.cx + Math.cos(angle) * distance, y: chartFrame.cy + Math.sin(angle) * distance };
      return `${point.x.toFixed(2)},${point.y.toFixed(2)}`;
    }).join(' ');
  }

  function areaPoints(metrics, values, progress = 1) {
    return metrics.map((metric, index) => {
      const point = radarPoint(index, metrics.length, values[metric.key] * progress);
      return `${point.x.toFixed(2)},${point.y.toFixed(2)}`;
    }).join(' ');
  }

  function springSvgAttribute(element, attribute, from, to, options, render) {
    runSpring(element, attribute, from, to, options, render);
  }

  function renderRadarChart(segments, selectedIndex = null) {
    if (!segments.length) return;
    const allKeys = new Set();
    segments.forEach((segment) => Object.keys(segment.scores || {}).forEach((key) => allKeys.add(key.toLowerCase())));
    const metrics = preferredEmotionOrder
      .filter((key) => allKeys.has(key))
      .map((key) => ({ key, label: key[0].toUpperCase() + key.slice(1) }));
    allKeys.forEach((key) => {
      if (!metrics.some((metric) => metric.key === key)) metrics.push({ key, label: key[0].toUpperCase() + key.slice(1) });
    });
    if (metrics.length < 3) {
      radarCard.classList.remove('is-visible');
      return;
    }

    const averageValues = Object.fromEntries(metrics.map(({ key }) => [
      key,
      segments.reduce((sum, segment) => sum + scoreValue(segment, key), 0) / segments.length * 100
    ]));
    const series = [{ label: 'Recording average', color: '#6258df', values: averageValues, source: null }];
    const selectedSegment = Number.isInteger(selectedIndex) ? segments[selectedIndex] : null;
    if (selectedSegment) {
      const windowValues = Object.fromEntries(metrics.map(({ key }) => [key, scoreValue(selectedSegment, key) * 100]));
      series.push({ label: `Window ${String(selectedIndex + 1).padStart(2, '0')}`, color: '#d9773f', values: windowValues, source: selectedSegment });
      radarWindowLegend.style.display = 'grid';
      radarWindowLabel.textContent = `Window ${String(selectedIndex + 1).padStart(2, '0')}`;
    } else {
      radarWindowLegend.style.display = 'none';
    }

    const cx = chartFrame.cx;
    const cy = chartFrame.cy;
    const radius = chartFrame.radius;
    const gridStagger = 0.08;
    const grid = [20, 40, 60, 80, 100].map((level, index) => {
      const points = gridPolygonPoints(metrics.length, level / 100);
      return `<g class="radar-grid-level" data-level="${index}" opacity="0" transform="translate(${cx} ${cy}) scale(0) translate(${-cx} ${-cy})"><polygon class="radar-grid-ring" points="${points}"/></g>`;
    }).join('');
    const axes = metrics.map((metric, index) => {
      const point = radarPoint(index, metrics.length, 100);
      return `<line class="radar-axis" data-axis="${index}" data-target-x="${point.x.toFixed(2)}" data-target-y="${point.y.toFixed(2)}" x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy}" aria-hidden="true"/>`;
    }).join('');
    const ticks = [20, 40, 60, 80, 100].map((level, index) => {
      const y = cy - radius * (level / 100) + 3;
      const delay = (5 * gridStagger * 0.5 + index * 0.06) * 1000;
      return `<text class="radar-tick" data-grid-label="${index}" data-delay="${delay}" x="${cx + 5}" y="${y.toFixed(2)}" opacity="0" aria-hidden="true">${level}</text>`;
    }).join('');
    const labels = metrics.map((metric, index) => {
      const angle = -Math.PI / 2 + (Math.PI * 2 * index) / metrics.length;
      const x = Math.cos(angle) * chartFrame.labelRadius;
      const y = Math.sin(angle) * chartFrame.labelRadius;
      const delay = (5 * gridStagger * 0.5 + index * gridStagger) * 1000;
      return `<g class="radar-label" data-label-index="${index}" data-target-x="${x.toFixed(2)}" data-target-y="${y.toFixed(2)}" data-delay="${delay}" transform="translate(0 0)" opacity="0"><text class="radar-axis-label" x="${cx}" y="${cy}">${escapeHtml(metric.label)}</text></g>`;
    }).join('');
    const areas = series.map((item, seriesIndex) => {
      const areaClass = seriesIndex === 0 ? 'radar-area is-average' : 'radar-area is-window';
      const delay = (5 * gridStagger + 0.2 + seriesIndex * 0.15) * 1000;
      const dataPoints = metrics.map((metric, index) => {
        const displayValue = item.values[metric.key];
        const point = radarPoint(index, metrics.length, 0);
        const rawValue = item.source ? scoreValue(item.source, metric.key) : averageValues[metric.key] / 100;
        const title = `${item.label} · ${metric.label}: raw score ${rawValue.toFixed(4)}; ${displayValue.toFixed(1)} on the 0–100 display scale`;
        return `<circle class="radar-point" data-point-index="${index}" data-target-x="${radarPoint(index, metrics.length, displayValue).x.toFixed(2)}" data-target-y="${radarPoint(index, metrics.length, displayValue).y.toFixed(2)}" cx="${point.x.toFixed(2)}" cy="${point.y.toFixed(2)}" r="4" fill="${item.color}" aria-hidden="true"><title>${escapeHtml(title)}</title></circle>`;
      }).join('');
      return `<g class="radar-series" data-series-index="${seriesIndex}" data-target-points="${areaPoints(metrics, item.values)}" data-delay="${delay}" opacity="0" transform="translate(${cx} ${cy}) scale(1) translate(${-cx} ${-cy})" role="img" tabindex="0" aria-label="${escapeHtml(item.label)} score area. Hover or focus to highlight."><polygon class="${areaClass}" points="${areaPoints(metrics, item.values, 0)}" fill="${item.color}" stroke="${item.color}"/><g>${dataPoints}</g></g>`;
    }).join('');

    radarChart.innerHTML = `
      <title id="radar-svg-title">emotion2vec+ emotion score radar chart</title>
      <desc id="radar-svg-desc">${metrics.map((metric) => metric.label).join(', ')} shown on a zero to one hundred display scale. The polygon compares the recording average${selectedSegment ? ' with the selected five-second window' : ''}. Scores are raw, uncalibrated model outputs, not probabilities.</desc>
      ${grid}${axes}${ticks}${areas}${labels}`;

    radarChart.querySelectorAll('.radar-grid-level').forEach((group, index) => {
      const apply = (scale) => {
        group.setAttribute('transform', `translate(${cx} ${cy}) scale(${scale}) translate(${-cx} ${-cy})`);
        group.setAttribute('opacity', String(Math.max(0, Math.min(1, scale))));
      };
      springSvgAttribute(group, 'grid-scale', 0, 1, { stiffness: 100, damping: 15, mass: 1, delay: index * gridStagger }, apply);
    });

    radarChart.querySelectorAll('.radar-axis').forEach((line, index) => {
      const targetX = Number(line.dataset.targetX);
      const targetY = Number(line.dataset.targetY);
      const apply = (progress) => {
        line.setAttribute('x2', String(cx + (targetX - cx) * progress));
        line.setAttribute('y2', String(cy + (targetY - cy) * progress));
      };
      springSvgAttribute(line, 'axis-progress', 0, 1, { stiffness: 80, damping: 15, mass: 1, delay: index * 0.05 }, apply);
    });

    radarChart.querySelectorAll('.radar-label').forEach((group) => {
      const targetX = Number(group.dataset.targetX);
      const targetY = Number(group.dataset.targetY);
      const apply = (progress) => group.setAttribute('transform', `translate(${targetX * progress} ${targetY * progress})`);
      springSvgAttribute(group, 'label-position', 0, 1, { stiffness: 80, damping: 15, mass: 1 }, apply);
      runTween(500, Number(group.dataset.delay), (opacity) => group.setAttribute('opacity', String(opacity)));
    });

    radarChart.querySelectorAll('.radar-tick').forEach((label) => {
      runTween(1100, Number(label.dataset.delay), (opacity) => label.setAttribute('opacity', String(opacity)));
    });

    radarChart.querySelectorAll('.radar-series').forEach((group) => {
      const seriesIndex = Number(group.dataset.seriesIndex);
      const delay = Number(group.dataset.delay);
      const polygon = group.querySelector('.radar-area');
      const points = Array.from(group.querySelectorAll('.radar-point'));
      runTween(150, delay, (opacity) => group.setAttribute('opacity', String(opacity)));
      runTween(1100, delay, (progress) => {
        const values = series[seriesIndex].values;
        polygon.setAttribute('points', areaPoints(metrics, values, progress));
        points.forEach((point, index) => {
          const targetX = Number(point.dataset.targetX);
          const targetY = Number(point.dataset.targetY);
          point.setAttribute('cx', String(cx + (targetX - cx) * progress));
          point.setAttribute('cy', String(cy + (targetY - cy) * progress));
        });
      });
    });

    function setHoveredSeries(hoveredIndex) {
      radarChart.querySelectorAll('.radar-series').forEach((group) => {
        const index = Number(group.dataset.seriesIndex);
        const scale = index === hoveredIndex ? 1.05 : 1;
        const opacity = hoveredIndex === null || index === hoveredIndex ? 1 : 0.3;
        group.style.transition = reducedMotion.matches ? 'none' : 'opacity 150ms ease';
        group.style.opacity = String(opacity);
        const currentScale = Number(group.dataset.scale || 1);
        runSpring(group, 'hover-scale', currentScale, scale, { stiffness: 400, damping: 25, mass: 1 }, (value) => {
          group.dataset.scale = String(value);
          group.setAttribute('transform', `translate(${cx} ${cy}) scale(${value}) translate(${-cx} ${-cy})`);
        });
        const area = group.querySelector('.radar-area');
        area.style.fillOpacity = index === hoveredIndex ? '.35' : '.15';
        area.style.strokeWidth = index === hoveredIndex ? '3' : '2';
        area.style.filter = index === hoveredIndex && !reducedMotion.matches ? `drop-shadow(0 0 12px ${area.getAttribute('stroke')})` : 'none';
        group.querySelectorAll('.radar-point').forEach((point) => {
          const from = Number(point.dataset.radius || 4);
          const to = index === hoveredIndex ? 6 : 4;
          runSpring(point, 'hover-radius', from, to, { stiffness: 300, damping: 20, mass: 1 }, (value) => {
            point.dataset.radius = String(value);
            point.setAttribute('r', String(value));
          });
        });
      });
    }

    radarChart.querySelectorAll('.radar-series').forEach((group) => {
      const index = Number(group.dataset.seriesIndex);
      group.addEventListener('mouseenter', () => setHoveredSeries(index));
      group.addEventListener('mouseleave', () => setHoveredSeries(null));
      group.addEventListener('focus', () => setHoveredSeries(index));
      group.addEventListener('blur', () => setHoveredSeries(null));
    });
    radarCard.classList.add('is-visible');
    radarCard.setAttribute('aria-hidden', 'false');
  }

  function setSelectedFile(file) {
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }

    selectedFileIsValid = false;
    fileValidationMessage = '';
    const extension = file?.name.split('.').pop()?.toLowerCase();
    if (!file || !['wav', 'mp3'].includes(extension)) {
      fileValidationMessage = 'Unsupported file type. Choose a .wav or .mp3 recording.';
      selectedFile.classList.remove('is-visible');
      audioPreview.classList.remove('is-visible');
      audioPreview.removeAttribute('src');
      fileReady.textContent = 'CHECK FILE';
      fileReady.className = 'file-ready';
      resetResults();
      updateControls();
      return;
    }

    fileName.textContent = file.name;
    fileSize.textContent = formatBytes(file.size);
    selectedFile.classList.add('is-visible');
    audioPreview.classList.remove('is-visible');
    audioPreview.removeAttribute('src');
    resetResults();

    if (file.size > MAX_FILE_BYTES) {
      fileValidationMessage = 'This file is larger than the 20 MiB limit.';
      fileReady.textContent = 'TOO LARGE';
      fileReady.className = 'file-ready';
      updateControls();
      return;
    }

    currentObjectUrl = URL.createObjectURL(file);
    audioPreview.src = currentObjectUrl;
    audioPreview.classList.add('is-visible');
    fileReady.textContent = 'CHECKING';
    fileReady.className = 'file-ready';

    const objectUrl = currentObjectUrl;
    audioPreview.onloadedmetadata = () => {
      if (objectUrl !== currentObjectUrl) return;
      if (Number.isFinite(audioPreview.duration) && audioPreview.duration > MAX_DURATION_SECONDS) {
        fileValidationMessage = 'This recording is longer than the 10-minute limit.';
        fileReady.textContent = 'TOO LONG';
        fileReady.className = 'file-ready';
      } else {
        selectedFileIsValid = true;
        fileReady.textContent = 'READY';
        fileReady.className = 'file-ready';
      }
      updateControls();
    };
    audioPreview.onerror = () => {
      if (objectUrl !== currentObjectUrl) return;
      // The server performs authoritative audio validation; unsupported preview codecs need not block analysis.
      selectedFileIsValid = true;
      fileReady.textContent = 'READY';
      fileReady.className = 'file-ready';
      updateControls();
    };

    updateControls();
  }

  function playSegment(startTime, endTime, button) {
    if (!audioPreview.src) return;
    const segmentIndex = Number(button?.dataset?.segmentIndex);
    if (Number.isInteger(segmentIndex) && activeSegments[segmentIndex]) {
      radarWindowSelect.value = String(segmentIndex);
      renderRadarChart(activeSegments, segmentIndex);
    }
    audioPreview.currentTime = Math.max(0, Number(startTime) || 0);
    activeSegmentEnd = Math.max(audioPreview.currentTime, Number(endTime) || audioPreview.duration);
    audioPreview.play().then(() => {
      if (button) button.setAttribute('aria-pressed', 'true');
    }).catch(() => {
      activeSegmentEnd = null;
      analyzeHelp.textContent = 'The browser could not play this preview. The analysis can still use the selected file.';
    });
  }
  window.playSegment = playSegment;

  audioPreview.addEventListener('timeupdate', () => {
    if (activeSegmentEnd !== null && audioPreview.currentTime >= activeSegmentEnd) {
      activeSegmentEnd = null;
      audioPreview.pause();
    }
  });

  function renderScores(scores) {
    const entries = Object.entries(scores || {});
    if (!entries.length) return '<p class="scores-title">No class scores returned</p>';
    const chips = entries.map(([label, score]) => {
      const numericScore = Number(score);
      const safeScore = Number.isFinite(numericScore) ? numericScore.toFixed(4) : '—';
      return `<span class="score-item"><span class="score-label">${escapeHtml(label)}</span><span class="score-val">${safeScore}</span></span>`;
    }).join('');
    return `<p class="scores-title">Uncalibrated class scores</p><div class="scores-list">${chips}</div>`;
  }

  function renderWindowLabelMix(segments) {
    const counts = new Map();
    segments.forEach((segment) => {
      const label = String(segment.label || 'unavailable').trim().toLowerCase() || 'unavailable';
      counts.set(label, (counts.get(label) || 0) + 1);
    });

    const total = segments.length;
    const entries = [...counts.entries()].sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]));
    windowLabelList.innerHTML = entries.map(([label, count]) => {
      const share = (count / total) * 100;
      return `<li class="window-label-row">
        <div class="window-label-topline"><span class="window-label-name">${escapeHtml(label)}</span><span class="window-label-share">${share.toFixed(1)}% · ${count}/${total}</span></div>
        <div class="window-label-track" aria-hidden="true"><span class="window-label-fill" style="width:${share.toFixed(2)}%"></span></div>
      </li>`;
    }).join('');
  }

  function renderResults(data) {
    const segments = Array.isArray(data.segments) ? data.segments : [];
    if (!segments.length) {
      resultsSummary.classList.remove('is-visible');
      resultsSummary.setAttribute('aria-hidden', 'true');
      voiceInterpretation.classList.remove('is-visible');
      voiceInterpretation.setAttribute('aria-hidden', 'true');
      windowLabelList.replaceChildren();
      radarCard.classList.remove('is-visible');
      radarCard.setAttribute('aria-hidden', 'true');
      showEmptyState('No segments were returned', 'The server completed the request but returned no review windows. Try another recording.');
      return;
    }

    activeSegments = segments;
    radarWindowSelect.replaceChildren(new Option('Recording average', ''));
    segments.forEach((segment, index) => {
      const start = Number(segment.start_seconds) || 0;
      const end = Number(segment.end_seconds) || start;
      const option = new Option(`Window ${String(index + 1).padStart(2, '0')} · ${start.toFixed(2)}–${end.toFixed(2)}s · ${segment.label || 'unknown'}`, String(index));
      radarWindowSelect.add(option);
    });
    radarWindowSelect.value = '';
    renderRadarChart(segments);

    summarySegments.textContent = String(segments.length);
    summaryDuration.textContent = `${Number(data.duration_seconds || 0).toFixed(1)}s`;
    summaryDevice.textContent = String(data.device || 'local');
    resultsSummary.classList.add('is-visible');
    resultsSummary.setAttribute('aria-hidden', 'false');
    renderWindowLabelMix(segments);
    voiceInterpretation.classList.add('is-visible');
    voiceInterpretation.setAttribute('aria-hidden', 'false');

    resultsContainer.className = 'timeline';
    resultsContainer.setAttribute('aria-busy', 'false');
    resultsContainer.innerHTML = segments.map((segment, index) => {
      const start = Number(segment.start_seconds) || 0;
      const end = Number(segment.end_seconds) || start;
      const label = segment.label || 'unavailable';
      const dataset = segment.dataset_label && segment.dataset_label !== 'unknown'
        ? `<span class="dataset-label">Dataset label: ${escapeHtml(segment.dataset_label)}</span>`
        : '';
      return `
        <article class="segment-card" style="animation-delay:${Math.min(index * 35, 280)}ms" aria-label="Window ${index + 1}, ${start.toFixed(2)} to ${end.toFixed(2)} seconds">
          <div class="segment-header">
            <div class="segment-time-wrap"><span class="segment-index">${String(index + 1).padStart(2, '0')}</span><span class="segment-time">${start.toFixed(2)}s – ${end.toFixed(2)}s</span></div>
            <button type="button" class="segment-play" data-start="${start}" data-end="${end}" data-segment-index="${index}" aria-pressed="false" aria-label="Play segment ${index + 1}">
              <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M5 3.8c0-.6.7-.9 1.2-.6l6.1 4.1c.5.3.5 1 0 1.4l-6.1 4.1c-.5.3-1.2 0-1.2-.6V3.8z"/></svg>Play segment
            </button>
          </div>
          <div class="emotion-row"><span class="emotion-caption">Estimated expression</span><span class="label-badge">${escapeHtml(label)}</span>${dataset}</div>
          ${renderScores(segment.scores)}
        </article>`;
    }).join('') + `
      <div class="model-meta">
        <strong>Model</strong> <code>${escapeHtml(data.model_id || 'emotion2vec+')}${data.model_revision ? ` · ${escapeHtml(data.model_revision)}` : ''}</code>
        &nbsp; <strong>Sample rate</strong> ${escapeHtml(data.sample_rate || '—')} Hz
        &nbsp; <strong>Window size</strong> ${escapeHtml(data.window_duration_seconds || 5)}s
      </div>`;

    resultsContainer.querySelectorAll('.segment-play').forEach((button) => {
      button.addEventListener('click', () => playSegment(button.dataset.start, button.dataset.end, button));
    });
  }

  radarWindowSelect.addEventListener('change', () => {
    const selectedIndex = radarWindowSelect.value === '' ? null : Number(radarWindowSelect.value);
    renderRadarChart(activeSegments, selectedIndex);
  });

  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      fileInput.click();
    }
  });
  fileInput.addEventListener('change', () => setSelectedFile(fileInput.files?.[0] || null));
  affirmationCheck.addEventListener('change', updateControls);

  ['dragenter', 'dragover'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add('is-dragover');
    });
  });
  ['dragleave', 'dragend'].forEach((eventName) => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove('is-dragover'));
  });
  dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropzone.classList.remove('is-dragover');
    const file = event.dataTransfer?.files?.[0];
    if (!file) return;
    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    setSelectedFile(file);
  });

  analyzeBtn.addEventListener('click', async () => {
    const file = fileInput.files?.[0];
    if (!file || !selectedFileIsValid || !affirmationCheck.checked || isAnalyzing) {
      updateControls();
      return;
    }

    isAnalyzing = true;
    progressPanel.classList.add('is-visible');
    progressPanel.setAttribute('aria-hidden', 'false');
    progressLabel.textContent = 'Analyzing audio segments';
    progressState.textContent = 'Working locally';
    resultsSummary.classList.remove('is-visible');
    resultsSummary.setAttribute('aria-hidden', 'true');
    voiceInterpretation.classList.remove('is-visible');
    voiceInterpretation.setAttribute('aria-hidden', 'true');
    radarCard.classList.remove('is-visible');
    radarCard.setAttribute('aria-hidden', 'true');
    resultsContainer.className = 'empty-state';
    resultsContainer.setAttribute('aria-busy', 'true');
    resultsContainer.innerHTML = '<div class="empty-inner"><span class="empty-icon" aria-hidden="true">…</span><p class="empty-title">Analysis in progress</p><p class="empty-copy">The local model is reviewing each five-second window.</p></div>';
    updateControls();

    try {
      const contentType = file.name.toLowerCase().endsWith('.mp3') ? 'audio/mpeg' : 'audio/wav';
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': contentType },
        body: file
      });
      let data;
      try { data = await response.json(); }
      catch { data = { detail: 'The local server returned an unreadable response.' }; }

      if (!response.ok) {
        resultsSummary.classList.remove('is-visible');
        resultsSummary.setAttribute('aria-hidden', 'true');
        voiceInterpretation.classList.remove('is-visible');
        voiceInterpretation.setAttribute('aria-hidden', 'true');
        resultsContainer.className = 'status-box status-error';
        resultsContainer.setAttribute('aria-busy', 'false');
        resultsContainer.textContent = data.detail || `Analysis failed (HTTP ${response.status}).`;
        progressState.textContent = 'Needs attention';
        return;
      }

      progressLabel.textContent = 'Analysis complete';
      progressState.textContent = 'Ready to review';
      renderResults(data);
      document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch {
      resultsSummary.classList.remove('is-visible');
      resultsSummary.setAttribute('aria-hidden', 'true');
      voiceInterpretation.classList.remove('is-visible');
      voiceInterpretation.setAttribute('aria-hidden', 'true');
      resultsContainer.className = 'status-box status-error';
      resultsContainer.setAttribute('aria-busy', 'false');
      resultsContainer.textContent = 'Could not reach the local CallSense server. Confirm that the app is running, then try again.';
      progressState.textContent = 'Server unavailable';
    } finally {
      isAnalyzing = false;
      updateControls();
      progressPanel.classList.remove('is-visible');
      progressPanel.setAttribute('aria-hidden', 'true');
    }
  });

  clearBtn.addEventListener('click', () => {
    fileInput.value = '';
    affirmationCheck.checked = false;
    selectedFileIsValid = false;
    fileValidationMessage = '';
    selectedFile.classList.remove('is-visible');
    audioPreview.pause();
    audioPreview.removeAttribute('src');
    audioPreview.load();
    audioPreview.classList.remove('is-visible');
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }
    progressPanel.classList.remove('is-visible');
    progressPanel.setAttribute('aria-hidden', 'true');
    resetResults();
    updateControls();
  });

  audioPreview.addEventListener('pause', () => {
    activeSegmentEnd = null;
    resultsContainer.querySelectorAll('.segment-play[aria-pressed="true"]').forEach((button) => button.setAttribute('aria-pressed', 'false'));
  });

  updateControls();
})();
