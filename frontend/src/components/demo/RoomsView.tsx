"use client";

import demoFloorplan from "@/data/flowdraft/demo_floorplan.json";

export function RoomsView() {
  const spaces = demoFloorplan.spaces || [];

  return (
    <div className="flex min-w-0 flex-1 flex-col overflow-auto bg-brand-surface p-6">
      <h2 className="mb-4 text-2xl font-semibold text-brand-navy">
        Rooms (Spaces)
      </h2>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {spaces.map((space, idx) => (
          <div
            key={space.space_id || idx}
            className="rounded-xl border border-brand-line bg-white p-4 shadow-sm"
          >
            <div className="mb-2 text-sm font-medium uppercase text-brand-subtle">
              {space.category}
            </div>
            <div className="text-lg font-semibold text-brand-ink">
              {space.space_id}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
