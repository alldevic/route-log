<template lang="pug">
  div.map-wrapper(
    :style="cssVars"
  )
    l-map#map(
      v-if="mapCoords"
      :zoom="15"
      :center="mapCoords"
    )
      l-tile-layer(
        url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
      )
      l-polygon(
        :latLngs="[points]"
      )
      template(v-for="(point, index) in trackPoints")
        l-marker(
          :key="index"
          :lat-lng="[point.lon, point.lat]"
        )
</template>

<script lang="ts">
// Import
import Vue from "vue";
import "leaflet/dist/leaflet.css";
import { Icon } from "leaflet";
import { LMap, LTileLayer, LPolygon, LMarker } from "vue2-leaflet";

// eslint-disable-next-line
//delete Icon.Default.prototype._getIconUrl;

const iconRetinaUrl = require("leaflet/dist/images/marker-icon-2x.png");
const iconUrl = require("leaflet/dist/images/marker-icon.png");
const shadowUrl = require("leaflet/dist/images/marker-shadow.png");

Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl
});

export default Vue.extend({
  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LMarker
  },
  props: {
    item: {
      type: Object,
      default: null
    },
    mapHeight: {
      type: Number,
      default: 340
    }
  },
  data: () => ({
    mapSettings: {
      lang: "ru_RU",
      coordorder: "latlong",
      version: "2.1"
    },
    points: null as any,
    mapCoords: null as any,
    geozone: null as any,
    trackPoints: null as any
  }),
  computed: {
    cssVars() {
      return {
        "--mapHeight": `${this.mapHeight}px`
      };
    }
  },
  watch: {
    item(value: any) {
      if (value) {
        this.geozone = value.geozone;
        const points = this.geozone.points.map(item => item.reverse());
        const [firstPoints] = points;
        this.points = points;
        this.mapCoords = firstPoints;
        this.trackPoints = value.track_points;
      }
    }
  }
});
</script>

<style lang="scss" scoped>
#map,
.map-wrapper {
  height: var(--mapHeight);
  width: 100%;
}

.map-wrapper {
  flex: 0 0 auto;
  position: relative;
}

// Media queries
@media screen and (max-height: 930px) {
  #map,
  .map-wrapper {
    height: calc(var(--mapHeight) - 60px);
  }
}

@media screen and (max-height: 850px) {
  #map,
  .map-wrapper {
    height: calc(var(--mapHeight) - 80px);
  }
}
</style>
