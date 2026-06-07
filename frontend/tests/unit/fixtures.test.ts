import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { EngineeringGraph } from '../../src/types';

const fixturesDir = path.join(__dirname, '..', 'fixtures', 'graphs');

describe('Graph Fixtures', () => {
  it('architecture fixture is valid', () => {
    const rawData = fs.readFileSync(path.join(fixturesDir, 'architecture_only.json'), 'utf8');
    const graph: EngineeringGraph = JSON.parse(rawData);
    expect(graph.meta.diagram_type).toBe('floorplan');
    expect(graph.spaces.length).toBeGreaterThan(0);
  });

  it('mep fixture is valid', () => {
    const rawData = fs.readFileSync(path.join(fixturesDir, 'mep_only.json'), 'utf8');
    const graph: EngineeringGraph = JSON.parse(rawData);
    expect(graph.meta.diagram_type).toBe('sld');
    expect(graph.fixtures.length).toBeGreaterThan(0);
  });

  it('fused fixture is valid', () => {
    const rawData = fs.readFileSync(path.join(fixturesDir, 'fused_graph.json'), 'utf8');
    const graph: EngineeringGraph = JSON.parse(rawData);
    expect(graph.meta.diagram_type).toBe('fused');
    expect(graph.spaces.length).toBeGreaterThan(0);
    expect(graph.fixtures.length).toBeGreaterThan(0);
  });
});
