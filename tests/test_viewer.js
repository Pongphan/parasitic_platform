// Regression checks run the shipped viewer JavaScript with a small DOM harness.
// Run: node tests/test_viewer.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../viewer_component/index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function createViewer() {
  const messages = [], frames = [], windowEvents = {}, nodes = {};
  let displayWidth = 450;
  const drawing = new Proxy({}, {get(target, key) { return target[key] || (() => {}); }});
  const wrap = {style:{}, getBoundingClientRect() {
    return {height:Math.min(displayWidth, Number.parseInt(this.style.maxWidth || '900')) + 220};
  }};
  function element(id) {
    if (!nodes[id]) nodes[id] = {
      style:{}, events:{}, disabled:id === 'calcBtn', textContent:id === 'viewerHint' ? 'Place target in center.' : '',
      tagName:id === 'cv' ? 'CANVAS' : 'BUTTON',
      addEventListener(type, fn) {this.events[type] = fn;},
      getContext() {return drawing;}, focus() {}, setPointerCapture() {},
      getBoundingClientRect() {
        const size = Math.min(displayWidth, Number.parseInt(wrap.style.maxWidth || '900'));
        return {left:10, top:20, width:size, height:size};
      },
    };
    return nodes[id];
  }
  class TestImage {
    constructor() {this.complete = false; this.naturalWidth = 0; this.naturalHeight = 0; this.loads = 0;}
    set src(value) {
      this._src = value; this.loads++;
      this.complete = true; this.naturalWidth = 1200; this.naturalHeight = 900;
      if(this.onload) this.onload();
    }
  }
  const parent = {postMessage(message) {messages.push(message);}};
  const window = {parent, addEventListener(type, fn) {windowEvents[type] = fn;}};
  const document = {getElementById:element, querySelector:() => wrap, activeElement:null};
  const context = vm.createContext({window, document, Image:TestImage, console,
    requestAnimationFrame(fn) {frames.push(fn);},
    ResizeObserver:class {observe() {}},
  });
  vm.runInContext(script, context);
  function flush() { while(frames.length) frames.shift()(); }
  flush();
  return {
    context, messages, nodes, flush,
    state() {return JSON.parse(vm.runInContext('JSON.stringify({zoom,panX,panY,vp,imageId})',context));},
    render(args, source=parent) {windowEvents.message({source,data:{type:'streamlit:render',args}}); flush();},
    eval(code) {const result = vm.runInContext(code,context); flush(); return result;},
    click(id) {element(id).events.click(); flush();},
    resize(width) {displayWidth = width; windowEvents.resize(); flush();},
    payloads() {return messages.filter(m => m.type === 'streamlit:setComponentValue').map(m => m.value);},
  };
}

const viewer = createViewer();
const firstArgs = {image_id:'image-a',image_b64:'AAAA',viewport:900,init_zoom:1,init_panX:0,init_panY:0};
viewer.render(firstArgs);
assert.equal(viewer.nodes.cv.width,900);
assert.equal(viewer.nodes.cv.style.width,undefined,'Canvas keeps responsive CSS width instead of fixed pixel CSS width.');
assert.equal(viewer.nodes.calcBtn.disabled,false);
viewer.eval('zoom=3;panX=120;panY=-80');
viewer.render(firstArgs);
assert.deepEqual(viewer.state(),{zoom:3,panX:120,panY:-80,vp:900,imageId:'image-a'},'An unrelated rerun must retain the framed ROI.');
assert.equal(viewer.eval('img.loads'),1,'Same-image reruns should not decode the image again.');
viewer.click('calcBtn');
viewer.render({...firstArgs,init_zoom:3,init_panX:120,init_panY:-80});
viewer.click('panRightBtn');
viewer.click('calcBtn');
assert.equal(viewer.payloads().length,2,'Consecutive Calculate clicks should both emit values.');
assert.equal(viewer.payloads()[1].image_id,'image-a');
assert.equal(viewer.payloads()[1].viewport,900);
assert.notEqual(viewer.payloads()[0].calc_token,viewer.payloads()[1].calc_token);
assert.equal(viewer.payloads()[1].panX,174);
viewer.render({...firstArgs,viewport:450});
assert.equal(viewer.state().panX,87,'Viewport changes scale pan to preserve image-space ROI.');
assert.equal(viewer.state().panY,-40);
assert.equal(viewer.state().zoom,3);
viewer.render({...firstArgs,image_id:'image-b',image_b64:'BBBB'});
assert.deepEqual(viewer.state(),{zoom:1,panX:0,panY:0,vp:900,imageId:'image-b'},'New images reinitialize the view.');
viewer.eval('zoom=4;panX=50;panY=20');
viewer.render({...firstArgs,image_id:'image-b',image_b64:'BBBB',reset_token:'reset-1'});
assert.equal(viewer.state().zoom,1,'Explicit reset tokens must reset the view.');
assert.equal(viewer.state().panX,0);
viewer.eval('zoom=2');
viewer.render({...firstArgs,image_id:'image-b',image_b64:'BBBB',reset_token:'reset-1'});
assert.equal(viewer.state().zoom,2,'Repeated reset tokens should not reset the view repeatedly.');
viewer.render({...firstArgs,image_id:'unauthorized'},{});
assert.equal(viewer.state().imageId,'image-b','Only the parent frame can send render updates.');

// A 900-pixel viewport displayed at 450 CSS pixels must map a 20px drag to 40px.
const responsive = createViewer();
responsive.render(firstArgs);
responsive.eval('onDown({clientX:100,clientY:100,pointerId:1,button:0});onMove({clientX:120,clientY:130});onUp();');
assert.equal(responsive.state().panX,40);
assert.equal(responsive.state().panY,60);
responsive.eval('panX=0;panY=0;zoom=1;onWheel({clientX:235,clientY:245,deltaY:-1,preventDefault(){}});');
assert.equal(responsive.state().zoom,1.08);
assert.equal(responsive.state().panX,0,'Wheel zoom at displayed center must retain center.');
assert.equal(responsive.state().panY,0);
const beforeResize = responsive.messages.filter(m => m.type === 'streamlit:setFrameHeight').at(-1).height;
responsive.resize(320);
const afterResize = responsive.messages.filter(m => m.type === 'streamlit:setFrameHeight').at(-1).height;
assert.ok(afterResize < beforeResize,'Iframe height must follow responsive content instead of logical viewport size.');
assert.equal(responsive.state().vp,900,'CSS resizing must not change the logical coordinates returned to Python.');
console.log('Viewer regression checks passed: state, image identity, consecutive clicks, reset, responsive drag/zoom, frame sizing.');
