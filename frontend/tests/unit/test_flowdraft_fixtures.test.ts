import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

describe('Flowdraft Fixtures', () => {
    it('should be valid JSON files', () => {
        const fixturesDir = path.resolve(__dirname, '../fixtures/flowdraft');
        const files = ['demo_floorplan.json', 'demo_compliance_report.json', 'demo_datacentre.json', 'mock_graph.json'];

        for (const file of files) {
            const filePath = path.join(fixturesDir, file);
            const content = fs.readFileSync(filePath, 'utf-8');
            const data = JSON.parse(content);
            expect(data).toBeDefined();
        }
    });
});
