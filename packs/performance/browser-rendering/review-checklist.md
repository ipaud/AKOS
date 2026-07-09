# Review Checklist — Browser Rendering Pack

## High

- [ ] Continuous/interactive animations use only transform/opacity. (BE1)
- [ ] No read-write-read-write layout thrashing patterns in loops. (BE2)
- [ ] Scroll-linked effects throttled via rAF or replaced with IntersectionObserver. (BE4)
- [ ] Large lists (>~100-200 items) virtualized. (BE5)

## Medium

- [ ] `will-change` applied narrowly and temporarily, not left on broadly. (BE3)
- [ ] CSS transitions/animations preferred over JS style-mutation loops where expressible. (BE6)
- [ ] Performance-critical interactions profiled with DevTools before considered complete. (BE7)

## Low

- [ ] DOM node count/depth reasonable for frequently-updated regions.
