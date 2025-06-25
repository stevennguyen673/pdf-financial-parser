import React, { useRef, useEffect, useState } from "react";
import * as d3 from "d3";
import { sankey, sankeyLinkHorizontal } from "d3-sankey";

export default function SankeyDiagram({ data, width = 700, height = 400 }) {
  const svgRef = useRef();
  const [tooltip, setTooltip] = useState({ visible: false, x: 0, y: 0, content: "" });

  useEffect(() => {
    if (!data) return;

    d3.select(svgRef.current).selectAll("*").remove();

    const sankeyGenerator = sankey()
      .nodeWidth(20)
      .nodePadding(15)
      .extent([[1, 1], [width - 1, height - 6]]);

    // Deep copy to avoid mutating props
    const graph = {
      nodes: data.nodes.map(d => ({ ...d })),
      links: data.links.map(d => ({ ...d })),
    };

    const { nodes, links } = sankeyGenerator(graph);

    // Create a color scale for categories (skip the root node)
    const color = d3.scaleOrdinal(d3.schemeCategory10)
      .domain(nodes.slice(1).map(d => d.name));

    // Assign colors to nodes (root is gray)
    nodes.forEach((node, i) => {
      node.color = i === 0 ? "#888" : color(node.name);
    });

    const svg = d3.select(svgRef.current);

    // Draw links, colored by target node
    svg.append("g")
      .selectAll("path")
      .data(links)
      .join("path")
      .attr("d", sankeyLinkHorizontal())
      .attr("fill", "none")
      .attr("stroke", d => d.target.color)
      .attr("stroke-width", d => Math.max(1, d.width))
      .attr("opacity", 0.5)
      .on("mousemove", function (event, d) {
        setTooltip({
          visible: true,
          x: event.clientX,
          y: event.clientY,
          content: (
            `<strong>${d.source.name} → ${d.target.name}</strong><br/>Value: ${d.value}`
          ),
        });
        d3.select(this).attr("opacity", 0.8);
      })
      .on("mouseleave", function () {
        setTooltip({ ...tooltip, visible: false });
        d3.select(this).attr("opacity", 0.5);
      });

    // Draw nodes
    svg.append("g")
      .selectAll("rect")
      .data(nodes)
      .join("rect")
      .attr("x", d => d.x0)
      .attr("y", d => d.y0)
      .attr("height", d => d.y1 - d.y0)
      .attr("width", d => d.x1 - d.x0)
      .attr("fill", d => d.color)
      .attr("stroke", "#333")
      .on("mousemove", function (event, d) {
        setTooltip({
          visible: true,
          x: event.clientX,
          y: event.clientY,
          content: (
            `<strong>${d.name}</strong><br/>Value: ${d.value}`
          ),
        });
        d3.select(this).attr("fill", d3.color(d.color).darker(0.7));
      })
      .on("mouseleave", function (event, d) {
        setTooltip({ ...tooltip, visible: false });
        d3.select(this).attr("fill", d.color);
      });

    // Node labels
    svg.append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .attr("x", d => d.x0 - 6)
      .attr("y", d => (d.y1 + d.y0) / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "end")
      .text(d => d.name)
      .filter(d => d.x0 < width / 2)
      .attr("x", d => d.x1 + 6)
      .attr("text-anchor", "start");

  }, [data, width, height]);

  return (
    <div style={{ position: "relative" }}>
      <svg ref={svgRef} width={width} height={height} />
      {tooltip.visible && (
        <div
          style={{
            position: "fixed",
            left: tooltip.x + 10,
            top: tooltip.y + 10,
            background: "rgba(0,0,0,0.85)",
            color: "#fff",
            padding: "8px 12px",
            borderRadius: "4px",
            pointerEvents: "none",
            zIndex: 10,
            fontSize: "14px",
            whiteSpace: "nowrap"
          }}
          dangerouslySetInnerHTML={{ __html: tooltip.content }}
        />
      )}
    </div>
  );
} 