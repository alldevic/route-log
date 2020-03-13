<template lang="pug">
  div.map-wrapper(
    :style="cssVars"
  )
    l-map#map(
      v-if="mapCoords"
      :zoom.sync="zoom"
      :center.sync="mapCoords"
      @update:center="centerUpdated"
    )
      l-tile-layer(
        url="http://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}"
      )

      l-polyline(
        :lat-lngs="[trackPoints]"
        :color="'blue'"
        :weight="1"
      )
      template(v-for="point in trackPoints")
        l-circle-marker(
          :lat-lng="point"
          :radius="2"
          :color="'blue'"
        )
          l-tooltip(:content="'' + point[2].split('+')[0]")

      l-polygon(
        :lat-lngs="[points]"
        :color="'orange'"
        :fillColor="'orange'"
      )

      template(v-for="point in points")
        l-circle-marker(
          :lat-lng="point"
          :radius="2"
          :color="'orange'"
        )
          l-tooltip(:content="geozone.name")
</template>

<script lang="ts">
// Import
import Vue from "vue";
import "leaflet/dist/leaflet.css";
import { Icon, latLng } from "leaflet";
import {
  LMap,
  LTileLayer,
  LPolygon,
  LPolyline,
  LTooltip,
  LCircleMarker
} from "vue2-leaflet";

type D = Icon.Default & {
  _getIconUrl: string;
};

delete (Icon.Default.prototype as D)._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

export default Vue.extend({
  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LPolyline,
    LTooltip,
    LCircleMarker
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
    zoom: 4,
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
        const points = this.geozone.points.map((item: any) => [
          item[1],
          item[0]
        ]);

        const [firstPoints] = points;
        this.points = points;
        this.mapCoords = latLng(firstPoints);

        this.trackPoints = value.track_points.map((item: any) => [
          item.point_value.lat,
          item.point_value.lon,
          item.utc
        ]);

        this.zoom = 15;
      }
    }
  },
  methods: {
    centerUpdated() {
      this.zoom = 15;
    },
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
  z-index: 1;
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
